def TempOfDat(i : float) -> str:
    """Расчет температуры по сигналу 4-20 мА с проверкой состояния датчика.
    i - сигнал датчика в мА
    Возврщает строку с состоянием датчика и рассчитанной температурой.
    """
    pv_max = 75.0
    pv_min = 0.0
    if i < 0:
        return {"status": "Датчик неисправен", "temperature": None}
    if i == 0:
        return {"status": "Датчик отключен", "temperature": None}
    if 0 < i <= 3.9:
        return {"status": "Датчик неисправен", "temperature": None}
    if i > 20:
        return {"status": "Датчик неисправен", "temperature": None}
    try:
        PV = (i-4) * (pv_max - pv_min) / 16 + pv_min
        return {"status": "Все ок", "temperature": PV}
    except Exception as e:
        return f"Ой все сломалось : {e}"



def cow_diagnostic(i : float):
    """Функция принимает на вход значение датчика
    и выдает результат в виде текстовой диганостити дачика и коровы
    """
    temp = TempOfDat(i)
    if temp["temperature"] < 35:
        return "Датчик свалился или корова плохо себя чувствует"
    if 35 <= temp["temperature"] < 37.5:
        return "Корова замерзла, нужно включить обогреватель"
    if 39.1 <= temp["temperature"] <=39.5:
        return "Корова перегрелась, нужно включить вентилятор"
    if temp["temperature"] >= 39.6:
        return "Срочно вызвать ветеринара, корова в критическом состоянии"
    if 37.5 <= temp["temperature"] < 39.0:
        return "Корова чувствует себя хорошо"


    
print (cow_diagnostic(4.5))