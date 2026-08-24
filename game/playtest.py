#!/usr/bin/env python3
"""Drive a complete run of MazeQuest Mini and screenshot every stage."""
import sys, time
from playwright.sync_api import sync_playwright

URL = 'file:///tmp/mazequest_app/MazeQuest-Mini.html'
KEY = {'u': 'ArrowUp', 'd': 'ArrowDown', 'l': 'ArrowLeft', 'r': 'ArrowRight'}
errors = []


def run(p):
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page(viewport={'width': 1060, 'height': 900})
    pg.on('pageerror', lambda e: errors.append('PAGEERROR: ' + str(e)))
    pg.on('console', lambda m: errors.append('CONSOLE ' + m.type + ': ' + m.text)
          if m.type == 'error' else None)
    pg.goto(URL)
    pg.wait_for_timeout(1800)

    def walk(s):
        for c in s:
            pg.keyboard.press(KEY[c])
            pg.wait_for_timeout(55)

    def act():
        pg.keyboard.press('e')
        pg.wait_for_timeout(220)

    def close_modal():
        btn = pg.query_selector('#modal [data-act]')
        if btn:
            btn.click()
            pg.wait_for_timeout(200)

    def objective():
        return pg.inner_text('#objective')

    def shot(name):
        pg.screenshot(path='/tmp/mazequest_app/shots/' + name + '.png')

    def check(label, cond):
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        if not cond:
            errors.append('CHECK FAILED: ' + label)

    # ---- menu ----
    shot('01-menu')
    check('menu wordmark renders', 'MazeQuest' in pg.inner_text('.wordmark'))

    # ---- how to play ----
    pg.click('[data-go="howto"]'); pg.wait_for_timeout(400)
    shot('02-howto')

    # ---- field desk ----
    pg.click('[data-go="menu"]'); pg.wait_for_timeout(300)
    pg.click('[data-go="custom"]'); pg.wait_for_timeout(1400)
    shot('03-desk-locked')
    check('12 loadout options render', len(pg.query_selector_all('.opt')) == 12)
    check('9 options start locked', len(pg.query_selector_all('.opt.locked')) == 9)
    check('field note written', 'standard-issue cap' in pg.inner_text('#notes-text'))

    # ---- start the run ----
    pg.click('#custom-back'); pg.wait_for_timeout(300)
    pg.click('[data-go="game"]'); pg.wait_for_timeout(700)
    shot('04-game-start')
    check('board built', len(pg.query_selector_all('.tile')) == 25 * 17)
    check('3 logs placed', len(pg.query_selector_all('.log')) == 3)
    check('12 pickups placed', len(pg.query_selector_all('.pickup')) == 12)

    # ---- notice ----
    walk('u'); act()
    check('notice modal opens', pg.query_selector('#modal h3') is not None)
    shot('05-notice')
    close_modal()

    # ---- meadow cache (loop A) ----
    walk('uuu'); walk('ll'); walk('uuu'); walk('rr')
    pg.wait_for_timeout(300)
    check('acorns 2 + crate A picked up', pg.inner_text('#n-acorns').startswith('2'))
    shot('06-meadow')

    # back out and east, with the spur detour
    walk('d'); walk('ll'); walk('dd'); walk('rr')
    walk('rrr'); walk('uu'); walk('dd'); walk('rrrr'); walk('u')
    check('reached the west bank', 'logs' in objective() or 'crossing' in objective())
    check('3 acorns', pg.inner_text('#n-acorns').startswith('3'))
    shot('07-riverbank')

    # ---- PUZZLE 1: the raft ----
    def nudge(log_id, path):
        pg.click('.log[data-log="%s"]' % log_id)
        pg.wait_for_timeout(140)
        for nx, ny in path:
            sel = '.nudge-dot[data-nx="%d"][data-ny="%d"]' % (nx, ny)
            pg.wait_for_selector(sel, timeout=3000)
            pg.click(sel)
            pg.wait_for_timeout(140)

    pg.click('.log[data-log="log0"]'); pg.wait_for_timeout(250)
    check('nudge targets appear on select', len(pg.query_selector_all('.nudge-dot')) > 0)
    shot('08-log-selected')
    pg.click('.log[data-log="log0"]'); pg.wait_for_timeout(150)   # deselect again
    nudge('log0', [(12, 8), (12, 9), (12, 10)])
    nudge('log2', [(13, 12), (13, 11), (13, 10)])
    nudge('log1', [(12, 13), (12, 12), (12, 11), (11, 11), (11, 10)])
    pg.wait_for_timeout(400)
    check('raft built', len(pg.query_selector_all('.log.locked')) == 3)
    shot('09-raft-built')

    # ---- cross to the shed (loop B) ----
    walk('rrrr')
    check('crossed the river', 'cabinet' in objective() or 'Shed' in objective())
    walk('ddd'); walk('rrr'); walk('rr'); walk('u'); walk('u')
    pg.wait_for_timeout(300)
    check('5 acorns + crate B', pg.inner_text('#n-acorns').startswith('5'))
    walk('d'); walk('l'); act()
    check('cabinet modal opens', pg.query_selector('#modal h3') is not None)
    check('4 forms taken', pg.inner_text('#n-forms') == '4')
    shot('10-cabinet')
    close_modal()

    # ---- PUZZLE 2: the permit gate ----
    walk('d'); walk('llll'); walk('uuuuuu')
    act()
    check('gate modal opens', pg.query_selector('[data-form]') is not None)
    shot('11-gate')
    pg.click('[data-form="1"]')            # deliberately wrong
    pg.wait_for_timeout(250)
    shot('12-denied')
    check('DENIED stamp shown', pg.query_selector('#denied:not([hidden])') is not None)
    pg.wait_for_timeout(900)
    act()
    pg.click('[data-form="0"]')            # correct
    pg.wait_for_timeout(400)
    check('gate opened', 'dam' in objective().lower())
    shot('13-gate-open')

    # ---- PUZZLE 3: the cracked dam ----
    walk('uuu')
    walk('l'); walk('d'); walk('u')                    # shim 2
    walk('lllll'); walk('d'); walk('r'); walk('l'); walk('u')   # shim 1 + acorn
    check('6 acorns', pg.inner_text('#n-acorns').startswith('6'))
    walk('rrrrrrrr'); walk('d'); walk('u')             # shim 3
    check('3 shims carried', pg.inner_text('#n-shims') == '3')
    shot('14-shims')
    walk('ll'); act()
    walk('ll'); act()
    walk('ll'); act()
    pg.wait_for_timeout(400)
    check('3 slots filled', len(pg.query_selector_all('.t-slot.filled')) == 3)
    check('flood drained', len(pg.query_selector_all('.t-flood')) == 0)
    shot('15-dam-fixed')

    # ---- exit ----
    walk('rrrrrrrrrr'); walk('u'); walk('r'); walk('l'); walk('uu')
    pg.wait_for_timeout(600)
    check('win screen shown', pg.query_selector('#scr-win.on') is not None)
    shot('16-win')
    if pg.query_selector('#scr-win.on'):
        print('  time   ', pg.inner_text('#win-time'))
        print('  acorns ', pg.inner_text('#win-acorns'))
        print('  nudges ', pg.inner_text('#win-nudges'))
        print('  denied ', pg.inner_text('#win-denied'))

    # ---- everything unlocked on the desk now ----
    pg.click('#scr-win [data-go="custom"]'); pg.wait_for_timeout(1500)
    check('all 12 items unlocked', len(pg.query_selector_all('.opt.locked')) == 0)
    shot('17-desk-unlocked')
    # swap the whole loadout and confirm the note rewrites
    pg.click('.opt[data-item="fedora"]'); pg.wait_for_timeout(200)
    pg.click('.opt[data-item="calipers"]'); pg.wait_for_timeout(200)
    pg.click('.opt[data-item="scarred"]'); pg.wait_for_timeout(1600)
    note = pg.inner_text('#notes-text')
    check('note rewrote for the new loadout',
          'traded fedora' in note and 'brass calipers' in note and 'scars' in note)
    print('  note:', note)
    shot('18-desk-swapped')

    b.close()


import os
os.makedirs('/tmp/mazequest_app/shots', exist_ok=True)
with sync_playwright() as p:
    run(p)

print('\n' + ('=' * 52))
if errors:
    print('%d PROBLEM(S):' % len(errors))
    for e in errors:
        print('  -', e)
    sys.exit(1)
print('Full playthrough completed with no errors.')
