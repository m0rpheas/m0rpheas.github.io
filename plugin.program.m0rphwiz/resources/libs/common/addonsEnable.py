import glob, os, sqlite3
import xbmc, xbmcaddon
from xbmc import log
from resources.libs.common.config import CONFIG
from datetime import datetime
from xml.dom.minidom import parse

def latest_db(db):
  if db in CONFIG.DB_FILES:
    match = glob.glob(os.path.join(CONFIG.DATABASE, '{0}*.db'.format(db)))
    comp = '{0}(.+?).db'.format(db[1:])
    highest = 0
    for file in match:
      try:
        check = int(re.compile(comp).findall(file)[0])
      except:
        check = 0
      if highest < check:
        highest = check
        return '{0}{1}.db'.format(db, highest)
  else:
    return False
        

addon_xmls = []

def enable_addons():
	for name in glob.glob(os.path.join(CONFIG.ADDONS,'*/addon.xml')):
		addon_xmls.append(name)
	addon_xmls.sort()
	addon_ids =[]
	for xml in addon_xmls:
		root = parse(xml)
		tag = root.documentElement
		_id = tag.getAttribute('id')
		addon_ids.append(_id)
	enabled=[]
	disabled=[]
	for x in addon_ids:
		try:
			xbmcaddon.Addon(id = x)
			enabled.append(x)
		except:
			disabled.append(x)
	for y in disabled:
		try:
			xbmc.executebuiltin(EnableAddon(y))
		except:
			enable_db(y)
	CONFIG.set_setting('first_postinstall', 'false')
	
def enable_db(d_addon):
    """ create a database connection to a SQLite database """
    dbfile = latest_db('Addons')
    dbfile = os.path.join(CONFIG.DATABASE, dbfile)
    conn = None
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    try:
    	c.execute("SELECT id, addonID, enabled FROM installed WHERE addonID = ?", (d_addon,))
    	found = c.fetchone()
    	if found == None:
    		# Insert a row of data
    		c.execute('INSERT INTO installed (addonID , enabled, installDate) VALUES (?,?,?)', (d_addon, '1', installed_date,))
    	else:
    		c.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (1, d_addon,))
    except Exception as e:
    	log('Failed to enable %s. Reason: %s' % (d_addon, e), xbmc.LOGINFO)
    conn.commit()
    conn.close()
