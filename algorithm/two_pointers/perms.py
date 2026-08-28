def checkInclusion(s1: str, s2: str) -> bool:
    len1, len2 = len(s1), len(s2)

    if len1 > len2:
        return False
    s1_count = [0] * 26
    s2_count = [0] * 26














    # Заполняем частоты для всей строки s1 и для самого первого окна в s2
    for i in range(len1):
        s1_count[ord(s1[i]) - ord('a')] += 1
        s2_count[ord(s2[i]) - ord('a')] += 1

    # Если первое же окно совпало, сразу возвращаем True
    if s1_count == s2_count:
        return True

    # Начинаем двигать скользящее окно по строке s2
    for i in range(len1, len2):
        # Добавляем новую букву в окно (справа)
        s2_count[ord(s2[i]) - ord('a')] += 1
        # Убираем старую букву из окна (слева)
        s2_count[ord(s2[i - len1]) - ord('a')] -= 1

        # Проверяем, совпал ли состав букв в текущем окне с s1
        if s1_count == s2_count:
            return True

    return False
