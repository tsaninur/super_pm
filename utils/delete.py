from utils.dbconfig import dbconfig
from rich import print as printc

def deleteEntry(sitename, username):
    db = dbconfig()
    cursor = db.cursor()

    # Query untuk memeriksa apakah entri ada
    query = "SELECT * FROM pm.entries WHERE sitename = %s AND username = %s"
    cursor.execute(query, (sitename, username))
    result = cursor.fetchone()

    if result:
        # Jika entri ditemukan, hapus
        delete_query = "DELETE FROM pm.entries WHERE sitename = %s AND username = %s"
        cursor.execute(delete_query, (sitename, username))
        db.commit()
        printc(f"[green][+] Entry for {sitename} with username {username} has been deleted successfully![/green]")
    else:
        printc("[red][!] Entry not found. No deletion performed.[/red]")
