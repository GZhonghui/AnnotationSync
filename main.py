import config, server, pdf_proc_pymupdf, os, curses
import message as m

def init_check():
    m.out("running check steps")

    check_result = True
    # local check
    local_sync_path = config.get_config("local_sync_path")
    local_sync_path = os.path.expanduser(local_sync_path)
    if not local_sync_path:
        m.out("fill local sync path")
        check_result = False
    elif not os.path.exists(local_sync_path):
        m.out("make sure local sync path exists")
        check_result = False
    elif os.path.isfile(local_sync_path):
        m.out("make sure local sync path is a dir")
        check_result = False

    # webdav server check
    url = config.get_config("webdav_url")
    username = config.get_config("webdav_username")
    password = config.get_config("webdav_password")
    server_path = config.get_config("webdav_datapath")

    if not url:
        m.out("fill webdav url")
        check_result = False
    if not username:
        m.out("fill webdav username")
        check_result = False
    if not password:
        m.out("fill webdav password")
        check_result = False
    if not server_path:
        m.out("fill server sync path")
        check_result = False

    if url and username and password:
        server_init_result = server.init_server()
        if not server_init_result:
            m.out("can not connect to server, check your config or network")
            check_result = False
        elif server_path:
            if not server.check_target_sync_exist():
                m.out("target sync path does not exist on webdav server")
                check_result = False

    return check_result

def precheck():
    if not init_check():
        m.out("check failed, exiting...")
        return False
    else:
        m.out("check passed")
    return True

def core(stdscr):
    local_sync_path = os.path.expanduser(config.get_config("local_sync_path"))
    local_files = os.listdir(local_sync_path)

    curses.curs_set(0)
    
    moves = {f: ' ' for f in local_files if f.endswith(".pdf")}
    options = [f for f in local_files if f.endswith(".pdf")] + ["Sync", "Exit"]
    current_row = 0
    
    def format_fixed_length(s, length):
        if len(s) > length:
            if length >= 1:
                return s[:length - 1] + '…'
            else:
                return '…'
        else:
            return s.ljust(length)

    def print_menu(current_row):
        stdscr.clear()
        # h, w = stdscr.getmaxyx()
        for idx, row in enumerate(options):
            # x = w//2 - len(row)//2
            # y = h//2 - len(options)//2 + idx
            x, y = 0, idx
            print_str = row
            if row != "Sync" and row != "Exit":
                print_str = f"{format_fixed_length(row, 24)} [{moves[row]}] Server"
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, print_str)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, print_str)
        stdscr.refresh()
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:
        print_menu(current_row)
        key = stdscr.getch()
        selected_item = options[current_row]

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == curses.KEY_LEFT and selected_item in moves.keys():
            moves[selected_item] = '<' if moves[selected_item] == ' ' else ' '
        elif key == curses.KEY_RIGHT and selected_item in moves.keys():
            moves[selected_item] = '>' if moves[selected_item] == ' ' else ' '
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_item == "Exit":
                break
            stdscr.clear()
            stdscr.addstr(0, 0, f"You selected '{options[current_row]}'")
            stdscr.refresh()
            stdscr.getch()
    
    stdscr.clear()

if __name__=='__main__':
    if True or precheck():
        curses.wrapper(core)