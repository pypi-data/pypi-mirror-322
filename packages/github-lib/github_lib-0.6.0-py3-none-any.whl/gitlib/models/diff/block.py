from pydantic import BaseModel


class DiffBlock(BaseModel):
    start: int
    a_path: str
    b_path: str

    def to_dict(self):
        return {"start": self.start, "a_path": self.a_path, "b_path": self.b_path}

    def __repr__(self):
        return f"DiffBlock(start={self.start}, a_path={self.a_path}, b_path={self.b_path})"
