class Pattern:
    """
    Pattern class used to represent all data related to the found patterns
    """

    def __init__(self, pattern_type, dataframe_segment, company_name, starting_date, ending_date, tendency, distance, points = None):
        """str: Type of the given pattern"""
        self.pattern_type = pattern_type
        """dataframe: Dataframe where the pattern was found"""
        self.dataframe_segment = dataframe_segment
        """str: Name of the company where the pattern was found"""
        self.company_name = company_name
        """str: Starting date of the pattern found"""
        self.starting_date = starting_date
        """str: Ending date of the pattern found"""
        self.ending_date = ending_date
        """Boolean: tendency of the pattern found (achieved or not)"""
        self.tendency = tendency
        """float: distance between the pattern found and the closest pattern in the dictionary"""
        self.distance = distance
        """Dataframe[]: points of interest to draw a line on the final canvas"""
        self.points = points

    def __str__(self):
        """Transforms the object to string"""
        return f'[{self.pattern_type}, {self.starting_date}, {self.ending_date}, {self.points}]'
