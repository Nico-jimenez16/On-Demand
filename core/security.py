from fastapi import Depends, Header, HTTPException


def get_current_user(x_user_id: int = Header(...), x_user_role: str = Header(...)):
    """
    El gateway añade headers:
      X-User-Id: id del usuario autenticado
      X-User-Role: client | provider
    """
    if not x_user_id or not x_user_role:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return {"id": x_user_id, "role": x_user_role}
