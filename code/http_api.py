import falcon
import pickledb

prefsDB = pickledb.load('prefs.db', True)

class Prefs:

    def on_get_pref(self, req, resp, uid, pref_key):
        """
        Returns: pref_key preference of a user if found
        """
        if (prefsDB.exists(uid) and prefsDB.dexists(uid, pref_key)):
            resp.media = prefsDB.dget(uid, pref_key) 
        else:
            resp.media = ""
        resp.status = falcon.HTTP_200

    def on_put_pref(self, req, resp, uid, pref_key):
        """
        Saves pref_key preference for a user
        """ 
        if not prefsDB.exists(uid):
            prefsDB.dcreate(uid)
        userPrefs = prefsDB.dadd(uid, [pref_key, req.media])
        resp.status = falcon.HTTP_200

    def on_get_prefs(self, req, resp, uid):
        """
        Returns: all prefs of a user if found
        """
        resp.media = prefsDB.get(uid) or ""
        resp.status = falcon.HTTP_200

    def on_get_all(self, req, resp):
        """
        Returns: IDs of all users with stored preferences 
        """
        resp.media = list(prefsDB.getall())
        resp.status = falcon.HTTP_200


app = falcon.API()
app.add_route('/prefs/{uid}/{pref_key}', Prefs(), suffix='pref')
app.add_route('/prefs/{uid}', Prefs(), suffix='prefs')
app.add_route('/prefs', Prefs(), suffix='all')

