import pandas as pd

def last5_to_points(last5_str):
    """
    Converts a Last 5 string into numeric form points.
    Example: "WinDrawDrawLossWin" -> 3+1+1+0+3 = 8
    """
    mapping = {"Win": 3, "Draw": 1, "Loss": 0}
    # Split the string every 3 or 4 characters
    last5_list = []
    temp = ""
    for c in last5_str:
        temp += c
        if temp in mapping:
            last5_list.append(temp)
            temp = ""
    # sum points
    return sum([mapping[result] for result in last5_list])

def load_standings():
    data = [
        # Club, MP, W, D, L, GF, GA, GD, Pts, Last5
        ("Arsenal",24,16,5,3,46,17,29,53,"WinDrawDrawLossWin"),
        ("Man City",24,14,5,5,49,23,26,47,"DrawDrawLossWinDraw"),
        ("Aston Villa",24,14,4,6,35,26,9,46,"WinDrawLossWinLoss"),
        ("Man United",24,11,8,5,44,36,8,41,"DrawDrawWinWinWin"),
        ("Chelsea",24,11,7,6,42,27,15,40,"DrawLossWinWinWin"),
        ("Liverpool",24,11,6,7,39,33,6,39,"DrawDrawDrawLossWin"),
        ("Brentford",24,11,3,10,36,32,4,36,"WinWinLossLossWin"),
        ("Fulham",24,10,4,10,34,35,-1,34,"DrawWinLossWinLoss"),
        ("Everton",24,9,7,8,26,27,-1,34,"LossDrawWinDrawDraw"),
        ("Newcastle",24,9,6,9,33,33,0,33,"WinWinDrawLossLoss"),
        ("Sunderland",23,8,9,6,24,26,-2,33,"DrawDrawLossWinLoss"),
        ("Bournemouth",24,8,9,7,40,43,-3,33,"LossWinDrawWinWin"),
        ("Brighton",24,7,10,7,34,32,2,31,"WinDrawDrawLossDraw"),
        ("Tottenham",24,7,8,9,35,33,2,29,"DrawLossLossDrawDraw"),
        ("Crystal Palace",24,7,8,9,25,29,-4,29,"LossDrawLossLossDraw"),
        ("Leeds United",24,6,8,10,31,42,-11,26,"DrawLossWinDrawLoss"),
        ("Nottm Forest",24,7,5,12,24,35,-11,26,"LossWinDrawWinDraw"),
        ("West Ham",24,5,5,14,29,48,-19,20,"LossLossWinWinLoss"),
        ("Burnley",23,3,6,14,25,44,-19,15,"LossLossDrawDrawDraw"),
        ("Wolves",24,1,5,18,15,45,-30,8,"LossDrawLossLossLoss")
    ]

    columns = ["Club","MP","W","D","L","GF","GA","GD","Pts","Last5"]
    df = pd.DataFrame(data, columns=columns)
    df["Form"] = df["Last5"].apply(last5_to_points)
    df.drop(columns="Last5", inplace=True)
    df.set_index("Club", inplace=True)
    return df
