def number_to_words(num):
    if not isinstance(num, int):
        raise ValueError("The input must be an integer.")

    # Define the number components
    feminine_units = ["", "אחת", "שתיים", "שלוש", "ארבע", "חמש", "שש", "שבע", "שמונה", "תשע"]
    units = ["", "אחד", "שניים", "שלושה", "ארבעה", "חמישה", "שישה", "שבעה", "שמונה", "תשעה"]
    feminine_big_units = ["", "", "שתי", "שלושת", "ארבעת", "חמשת", "ששת", "שבעת", "שמונת", "תשעת"]
    big_units = ["", "", "שני", "שלוש", "ארבע", "חמש", "שש", "שבע", "שמונה", "תשע"]
    
    feminine_teens = ["עשר", "אחת עשרה", "שתיים עשרה", "שלוש עשרה", "ארבע עשרה", "חמש עשרה", "שש עשרה", "שבע עשרה", "שמונה עשרה", "תשע עשרה"]
    teens = ["עשרה", "אחד עשר", "שניים עשר", "שלושה עשר", "ארבעה עשר", "חמישה עשר", "שישה עשר", "שבעה עשר", "שמונה עשר", "תשעה עשר"]
    
    tens = ["", "", "עשרים", "שלושים", "ארבעים", "חמישים", "שישים", "שבעים", "שמונים", "תשעים"]
    hundreds = ["", "מאה", "מאתיים", "שלוש מאות", "ארבע מאות", "חמש מאות", "שש מאות", "שבע מאות", "שמונה מאות", "תשע מאות"]
    big_numbers = ["", "אלף", "מיליון", "מיליארד", "טריליון", "קוואדריליון", "קוונטיליון", "סקסטיליון", "ספטיליון", "אוקטיליון", "נוניליון"]

    # Handle zero
    if num == 0:
        return "אפס"

    # Break the number into chunks of 3 digits each
    def chunk_number(n):
        parts = []
        while n > 0:
            parts.append(n % 1000)
            n //= 1000
        return parts[::-1]

    def chunk_to_words(chunk, big_numbers=False, feminine=False):
        words = []
        su = feminine_units if feminine else units
        bgu = feminine_big_units if feminine else big_units
        unts = bgu if big_numbers else su
        tns = feminine_teens if feminine else teens
        add_ve = False
        if chunk >= 100:
            words.append(hundreds[chunk // 100])
            chunk %= 100
            add_ve = True
        if 10 <= chunk < 20:
            t = tns[chunk - 10]
            if add_ve:
                t = "ו" + t
            words.append(t)
        else:
            if chunk >= 20:
                t=tens[chunk // 10]
                words.append(t)
                chunk %= 10
            if chunk > 0:
                if len(words) > 0:
                    words.append(f"ו{unts[chunk]}")
                else:
                    words.append(unts[chunk])

        return " ".join(words)

    # Handle "and" for special cases
    def handle_special_cases(parts):
        result = []
        add_ve = False
        for i, part in enumerate(parts):
            text = ''
            if part == 0 and i > 0:
                continue
            scale = len(parts) - i - 1
            if scale == 1 and part == 1:
                text = big_numbers[scale]  # "מיליון" and "אלף"
            else:
                if scale > 1:
                    text = chunk_to_words(part, big_numbers=True)
                else:
                    text = chunk_to_words(part)
            if scale > 0 and part > 0:
                text = text + " " + big_numbers[scale]
            if i + 1 == (len(parts) - 1 if (len(parts) != 2 and parts[len(parts) - 1] == 0) else len(parts)) and len(parts) > 1:
                text = "ו" + text
            result.append(text)
        return result

    # Split number into chunks
    parts = chunk_number(num)
    words = handle_special_cases(parts)
    
    special_cases = {
        "שניים אלף": "אלפיים",
    }
    
    for i, word in enumerate(words):
        if word in special_cases:
            words[i] = special_cases[word]

    # Join words with correct punctuation
    result = " ".join(words).strip()
    return result