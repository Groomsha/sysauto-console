class LVMMenu:
    def __init__(self) -> None:
        pass

    @staticmethod
    def main_menu() -> str:
        return """
        P - Physical Volume Info/Create
        L - Logical Volume Info/Create
        Q - Exit\n"""

    @staticmethod
    def physical_menu() -> str:
        return """
        I - Physical Volume Info
        C - Physical Volume Create
        D - Physical Volume Remove
        R - Return
        Q - Exit\n"""

    @staticmethod
    def logical_menu() -> str:
        return """
        I - Logical Volume Info
        C - Logical Volume Create
        U - Logical Volume Resize
        D - Logical Volume Remove
        R - Return
        Q - Exit\n"""
