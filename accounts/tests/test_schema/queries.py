register_user = """
    mutation RegisterUser($registerInfo: RegisterInput!) {
      register(registerInfo: $registerInfo) {
        success
      }
    }
"""

logout_user = """
    mutation LogoutUser {
        logout {
            success
        }
    }
"""
