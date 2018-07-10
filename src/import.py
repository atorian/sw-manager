import pymysql
from swarfarm import load_profile

runes = load_profile('/Users/hcdeveloper/src/swop/atorian-1757319.json')

db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    port=32776,
    db='swop',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:

    data = [(rune.id, rune.set.name, rune['hp%'], rune['hp'], rune['atk%'], rune['atk'], rune['def%'], rune['def'],
             rune['spd'], rune['cr'], rune['cd'], rune['acc'], rune['res']) for rune in runes]

    with db.cursor() as c:
        sql = '''
        insert into runes(`id`, `rune_set`, hp, hp_flat, atk, atk_flat, def, def_flat, spd, cr, cd, acc, res)
        values '''
        rows = []
        row = '({}, "{}", {},' + ', '.join(['{}'] * 10) + ')'
        for rune in runes:
            rows.append(row.format(
                rune.id,
                rune.set.name,
                rune['hp%'],
                rune['hp'],
                rune['atk%'],
                rune['atk'],
                rune['def%'],
                rune['def'],
                rune['spd'],
                rune['cr'],
                rune['cd'],
                rune['acc'],
                rune['res']
            ))

        print(sql + ', '.join(rows))
        c.execute(sql + ', \n'.join(rows))

    db.commit()
finally:
    db.close()
