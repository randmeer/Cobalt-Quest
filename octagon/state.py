class State:
    def _execute(self) -> str:
        """called by octagon.run"""
        returnvalue = self.execute()
        if type(returnvalue) != str:
            raise Exception(f"Running '{self.__class__.__name__}.execute()' did not return instruction string")
        return returnvalue

    def execute(self) -> str:
        pass

