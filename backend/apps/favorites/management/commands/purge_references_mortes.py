"""
Supprime les favoris, commentaires et notes qui désignent un objet disparu.

Ces trois tables visent leur cible par un couple (type, reference_id) plutôt
que par une clé étrangère : la base ne peut ni refuser une référence invalide,
ni supprimer en cascade quand la cible disparaît.

Depuis apps/references.py l'écriture est validée, et `sync_matches` lance ce
nettoyage après chaque purge de matchs. Cette commande reste utile pour un
contrôle manuel, notamment avec --dry-run.
"""

from django.core.management.base import BaseCommand

from apps.references import purge_dead_references


class Command(BaseCommand):
    help = "Supprime les favoris, commentaires et notes pointant vers un objet inexistant"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Affiche ce qui serait supprimé, sans rien supprimer.",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        resultat = purge_dead_references(dry_run=dry_run)
        total = sum(resultat.values())

        for libelle, nombre in resultat.items():
            self.stdout.write(f'{libelle} : {nombre} orphelin(s)')

        if total == 0:
            self.stdout.write(self.style.SUCCESS('\nAucune référence morte.'))
        elif dry_run:
            self.stdout.write(self.style.WARNING(
                f'\n{total} référence(s) morte(s) — rien supprimé (--dry-run).'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n{total} référence(s) morte(s) supprimée(s).'))
