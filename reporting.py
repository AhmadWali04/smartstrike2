import pandas as pd

def generate_report(person,case):
    """
    Generate an empty we can store round data to     
    -----
    Parameters:
    person: Red || Blue boxer that we are creating report for
    case: Are we reporting on shadowboxing? Or Rounds?
    """
    df = pd.DataFrame()
    df['Left Thrown'] = 0
    df['Right Thrown'] = 0
    df['Head Covered Time'] = 0
    df['Good Footwork Time'] = 0
    df['Uppercuts Thrown'] = 0
    df['Hooks Thrown'] = 0
    df['Jabs Thrown'] = 0
    df['Crosses Thrown'] = 0
    if case == 1: #If shadowboxing
        None
    if case == 2: #If sparring, more stats to track
        df['Headshots Absorbed'] = 0
        df['Bodyshots Absorbed'] = 0
        df['Headshots Landed'] = 0
        df['Bodyshots Landed'] = 0
        df['Parries'] = 0
        df['Slips'] = 0
        df['Blocks'] = 0



def outout_report(person,df, case):
    """
    Outputs final reports for our person
    -----
    :param person: Description
    :param df: Description
    :param case: Description
    """
    if case == 1: #If shadowboxing
        df['Strikes Thrown'] = df['Left Hand Punches'] + df['Right Hand Punches']
        df['Strike Efficiency Percentage'] = df['Strikes Thrown'] / df['Strikes Landed']
    if case == 2: #If sparring
        df['Strikes Absorbed'] = df['Headshots Absorbed'] + df['Bodyshots Absorbed']
        df['Strikes Landed'] = df['Headshots Landed'] + df['Bodyshots Landed']
