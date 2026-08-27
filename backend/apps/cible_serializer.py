"""
Traduction entre le couple (type, reference_id) de l'API et les clés
étrangères de la base.

L'API publique n'a pas bougé quand les références polymorphes sont devenues de
vraies clés étrangères : le front envoie toujours `type` et `reference_id`, et
les relit tels quels. Toute la conversion tient ici.
"""

from rest_framework import serializers

from apps.references import REFERENCE_TYPES, champ_de, resolve_reference


class CibleReferenceSerializerMixin(serializers.Serializer):
    """
    À combiner avec un ModelSerializer dont le modèle hérite de CibleReference.

    En écriture : (type, reference_id) → l'instance visée, placée dans le bon
    champ de liaison. En lecture : le chemin inverse.
    """

    type = serializers.ChoiceField(choices=REFERENCE_TYPES, write_only=True)
    reference_id = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        type_ = attrs.pop('type', None)
        ref = attrs.pop('reference_id', None)

        # Champs absents : DRF a déjà signalé le manque avant d'arriver ici.
        if type_ is None or ref is None:
            return attrs

        cible = resolve_reference(type_, ref)
        if cible is None:
            raise serializers.ValidationError({
                'reference_id': (
                    f"Aucun objet de type « {type_} » ne porte la référence « {ref} »."
                )
            })

        attrs[champ_de(type_)] = cible
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = instance.type
        data['reference_id'] = instance.reference_id
        return data


def filtrer_par_cible(queryset, type_: str | None, reference_id: str | None):
    """
    Applique les filtres `?type=` et `?reference_id=` d'une vue liste.

    Une référence introuvable ne renvoie pas une erreur mais une liste vide :
    c'est une consultation, pas une écriture.
    """
    if not type_:
        return queryset

    champ = champ_de(type_)
    if champ is None:
        return queryset.none()

    if not reference_id:
        return queryset.filter(**{f'{champ}__isnull': False})

    cible = resolve_reference(type_, reference_id)
    if cible is None:
        return queryset.none()

    return queryset.filter(**{champ: cible})
