/**
 * Creates the bee field log spreadsheet and the endpoint the field log posts to.
 *
 * This is Google Apps Script, not part of the website build. It is the same idea
 * as tools/create-notes-form.gs: the structure lives in the repo as code, so a
 * deleted sheet or a new season means re-running this rather than rebuilding
 * from memory.
 *
 * WHY NOT A GOOGLE FORM, like the after-class notes?
 *
 * A form submission is one response. A morning's counting is twenty observations
 * that all share one set of session details, and the log has to be able to send
 * them together, after the fact, from a phone that had no signal in the garden.
 * So this is a small web app instead: the field log posts JSON, and this appends
 * one row per observation.
 *
 * Everything else matches the notes form. No logins, no email collection, the
 * coach owns the sheet, and first names only.
 *
 * HOW TO RUN
 *   1. Go to https://script.google.com and click "New project".
 *   2. Delete the sample code, paste this whole file in, and save.
 *   3. Pick "createFieldLogSheet" in the function dropdown and click Run.
 *   4. Authorise it when asked. That prompt is your own account creating your
 *      own spreadsheet; it is expected.
 *   5. Open "Execution log" and copy the SHEET URL it prints.
 *
 * THEN DEPLOY IT, which is the part that is easy to miss:
 *   6. Deploy > New deployment > gear icon > Web app.
 *   7. Execute as: Me.  Who has access: Anyone.
 *   8. Deploy, authorise again, and copy the Web app URL.
 *   9. Paste that URL into SHEET_ENDPOINT in
 *      innovation-project/field-log.html, and commit it.
 *
 * "Anyone" is required. The kids are not signed in to Google on a phone in a
 * garden, and we do not want them to have to be. The URL is unguessable, the
 * endpoint only ever appends, and it never reads anything back out.
 *
 * AFTER ANY EDIT to this script you must Deploy > Manage deployments > edit >
 * New version. Saving alone does not change what the live URL runs.
 */

var SHEET_NAME = 'Observations';
var FOLDER_NAME = 'FLL BIOGLOW — Bee field log photos';

// The same columns as the CSV the field log exports, in the same order, with one
// difference: the CSV's `has_photo` says yes or no, because at export time the
// photo is still on the phone. Here it is a link to the file in Drive.
var HEADERS = [
  'submitted_at', 'record_id', 'site', 'date', 'observer', 'recorder',
  'transect_ft', 'start_temp_F', 'start_wind_mph', 'sky', 'time_seen',
  'visitor_type', 'bee_group', 'bee_subgroup', 'label', 'count', 'plant',
  'description', 'photo'
];


function createFieldLogSheet() {
  var ss = SpreadsheetApp.create('FLL BIOGLOW — Bee field log');
  var sheet = ss.getSheets()[0];
  sheet.setName(SHEET_NAME);

  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, HEADERS.length);

  // Photos go in a folder of their own. It is left PRIVATE on purpose: a garden
  // photo can catch somebody in the background, and this repo's rule is that
  // pictures of children stay off anything public. Share it with the people who
  // need it, by hand, the same way you would share any other folder.
  var folder = DriveApp.createFolder(FOLDER_NAME);

  var props = PropertiesService.getScriptProperties();
  props.setProperty('SHEET_ID', ss.getId());
  props.setProperty('FOLDER_ID', folder.getId());

  Logger.log('--- Bee field log ---');
  Logger.log('SHEET URL:  ' + ss.getUrl());
  Logger.log('PHOTO FOLDER: ' + folder.getUrl());
  Logger.log('');
  Logger.log('Next: Deploy > New deployment > Web app.');
  Logger.log('  Execute as: Me');
  Logger.log('  Who has access: Anyone');
  Logger.log('Then paste the Web app URL into SHEET_ENDPOINT in');
  Logger.log('innovation-project/field-log.html');
  Logger.log('');
  Logger.log('The photo folder is private. Share it with whoever needs it.');
}


/** Receives a batch of observations from the field log. */
function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var session = payload.session || {};
    var records = payload.records || [];

    if (!records.length) {
      return _json({ ok: false, error: 'no records' });
    }

    var props = PropertiesService.getScriptProperties();
    var sheetId = props.getProperty('SHEET_ID');
    if (!sheetId) {
      return _json({ ok: false, error: 'run createFieldLogSheet first' });
    }
    var folder = _photoFolder(props);

    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(SHEET_NAME);
    var now = new Date();
    var photos = 0;

    var rows = records.map(function (r) {
      var photoCell = '';
      if (r.photo) {
        var url = _savePhoto(folder, r.id, r.photo);
        if (url) {
          photoCell = url;
          photos++;
        } else {
          photoCell = 'upload failed';
        }
      }
      return [
        now, r.id, session.site, session.date, session.observer,
        session.recorder, session.transect, session.temp, session.wind,
        session.sky, r.seenAt, r.type, r.group, r.sub, r.label, r.count,
        r.plant, r.desc, photoCell
      ];
    });

    sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, HEADERS.length)
      .setValues(rows);

    return _json({ ok: true, saved: rows.length, photos: photos });
  } catch (err) {
    return _json({ ok: false, error: String(err) });
  }
}


/** Writes one data-URL photo into Drive and returns a link to it. */
function _savePhoto(folder, recordId, dataUrl) {
  if (!folder) { return ''; }
  try {
    var comma = dataUrl.indexOf(',');
    if (comma < 0) { return ''; }
    var meta = dataUrl.substring(0, comma);
    var type = meta.substring(meta.indexOf(':') + 1, meta.indexOf(';'));
    var bytes = Utilities.base64Decode(dataUrl.substring(comma + 1));
    var blob = Utilities.newBlob(bytes, type, recordId + '.jpg');
    // A repeat send would otherwise pile up duplicates of the same record.
    var existing = folder.getFilesByName(recordId + '.jpg');
    if (existing.hasNext()) { return existing.next().getUrl(); }
    return folder.createFile(blob).getUrl();
  } catch (err) {
    return '';
  }
}


function _photoFolder(props) {
  var id = props.getProperty('FOLDER_ID');
  if (id) {
    try { return DriveApp.getFolderById(id); } catch (err) { /* deleted */ }
  }
  var folder = DriveApp.createFolder(FOLDER_NAME);
  props.setProperty('FOLDER_ID', folder.getId());
  return folder;
}


/** A GET is only ever somebody checking the URL works. */
function doGet() {
  return _json({ ok: true, message: 'Bee field log endpoint. POST to it.' });
}


function _json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
