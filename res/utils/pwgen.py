class PWGenerator():
    
    def __init__(self, length: int = 12, *args, **kwargs) -> None:
        """
        Set total length of password

        Args:
            length (int, optional): Length of the random password. Defaults to 12.
        """
        # Length of generated password
        self.length = length
        
        # Set default values
        self.lower_case_letters = True
        self.upper_case_letters = True
        self.digits = True
        self.symbols = True
        
        # Set values from kwargs
        kwargs_parameters = ["lower_case_letters", "upper_case_letters", "digits", "symbols"]
        for param in kwargs_parameters:
            if param in kwargs:
                setattr(self, param, kwargs[param])
                
        self._init_all_chars()
        
    def _init_all_chars(self):
        """
        Initializes string of all posible characters
        """
        import string
        self._all_chars_list = []
        if self.lower_case_letters:
            self._all_chars_list.append(string.ascii_letters[:len(string.ascii_letters)//2])
        if self.upper_case_letters:
            self._all_chars_list.append(string.ascii_letters[len(string.ascii_letters)//2:])
        if self.symbols:
            self._all_chars_list.append(string.punctuation)
        if self.digits:
            self._all_chars_list.append(string.digits)
        self._all_chars = "".join(self._all_chars_list)
        
    def get_random_password(self) -> str:
        """
        Returns a random password of length self.Length

        Returns:
            str: Random string representing password
        """
        import random
        password = ""
        for _ in range(self.length):
            password += random.choice(self._all_chars)
        return password