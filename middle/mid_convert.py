from back.convert import convert_value
import eel

@eel.expose
def convert_date_py(decision_date):
    return convert_value(decision_date)
