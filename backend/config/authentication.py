from rest_framework_simplejwt.authentication import JWTAuthentication


class SoftJWTAuthentication(JWTAuthentication):
    """
    Comme JWTAuthentication mais ne lève pas d'exception si le token est
    invalide ou expiré — retourne None (utilisateur anonyme).
    Cela permet aux endpoints AllowAny de fonctionner même si le client
    envoie un token périmé.
    """
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except Exception:
            return None
