from utils.add import computeMasterKey
from utils.dbconfig import dbconfig
import utils.aesutil

def updateEntry(master_password, salt, sitename, username, new_password):
    # Compute master key
    mk = computeMasterKey(master_password, salt)

    # Encrypt the new password with the master key
    encrypted_password = utils.aesutil.encrypt(key=mk, source=new_password, keyType="bytes")

    # Update password in the database
    db = dbconfig()
    cursor = db.cursor()
    query = "UPDATE pm.entries SET password = %s WHERE sitename = %s AND username = %s"
    val = (encrypted_password, sitename, username)
    cursor.execute(query, val)
    db.commit()

    if cursor.rowcount > 0:
        return True  # Password updated successfully
    else:
        return False  # No matching entry found
