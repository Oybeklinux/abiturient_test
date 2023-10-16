def row_2_col(rows, col=2):
    row_list = []
    lst = []
    i = 0
    for row in rows:
        i += 1
        lst.append(row)
        if i % col == 0:
            row_list.append(lst)
            lst = []
    if i % col != 0:
        row_list.append(lst)

    return row_list
