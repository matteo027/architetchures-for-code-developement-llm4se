def sort_numbers(numbers: str) -> str:
    word_to_num = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    num_to_word = {value: key for key, value in word_to_num.items()}

    words = numbers.split()
    int_list = [word_to_num.get(word, None) for word in words]
    filtered_list = [num for num in int_list if num is not None]

    if not filtered_list:
        return ''

    sorted_list = sorted(set(filtered_list))
    result_list = [num_to_word[num] for num in sorted_list]
    return ' '.join(result_list)