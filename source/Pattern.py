class Pattern:
    """
    Pattern class used to represent all data related to the found patterns
    """

    def __init__(self, pattern_type, dataframe_segment, company_name, starting_date, ending_date, tendency):
        self.pattern_type = pattern_type
        """str: Type of the given pattern"""
        self.dataframe_segment = dataframe_segment
        """str: Name of the company where the pattern was found"""
        self.company_name = company_name
        """dataframe: Sataframe where the pattern was found"""
        self.starting_date = starting_date
        """str: Starting date of the pattern found"""
        self.ending_date = ending_date
        """str: Ending date of the pattern found"""
        self.tendency = tendency
        """Boolean: tendency of the pattern found (achieved or not)"""

    def __str__(self):
        """Transforms the object to string"""
        return f'[{self.pattern_type}, {self.starting_date}, {self.ending_date}]'
