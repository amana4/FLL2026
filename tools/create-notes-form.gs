/**
 * Creates the after-class notes form in one run, instead of clicking twelve
 * questions into the Google Forms UI by hand.
 *
 * This is Google Apps Script, not part of the website build. It exists so the
 * form's structure is written down as code: if the form is ever deleted or you
 * want a fresh one next season, re-run this rather than rebuilding from memory.
 *
 * HOW TO RUN
 *   1. Go to https://script.google.com and click "New project".
 *   2. Delete the sample code, paste this whole file in, and save.
 *   3. Pick "createNotesForm" in the function dropdown and click Run.
 *   4. Google will ask you to authorise it the first time. That prompt is for
 *      your own account creating your own form; it is expected.
 *   5. Open "Execution log" and copy the EMBED URL it prints.
 *
 * AFTERWARDS, in the Forms UI:
 *   - Check the form is published and that responder access is "Anyone with the
 *     link". Google changed this in late 2024 and a script-created form may
 *     start unpublished, which would mean nobody can submit.
 *   - Responses tab, Sheets icon, to create the linked spreadsheet.
 *
 * Question 2 uses Kid 1 to Kid 5 rather than real names on purpose: notes get
 * copied into the repo, and the repo is public.
 */

function createNotesForm() {
  var form = FormApp.create('FLL BIOGLOW — After-class notes');

  form.setDescription(
    'Five minutes after a session. You do not have to fill in every box — one ' +
    'good sentence beats five blank fields. Use Kid 1 to Kid 5 rather than ' +
    'real names.'
  );

  // No email collection, so no login is needed. That is what lets the younger
  // kids submit at all, and it keeps children's addresses out of the sheet.
  form.setCollectEmail(false);
  form.setAllowResponseEdits(true);
  form.setLimitOneResponsePerUser(false);

  // 1. Session date, separate from the automatic submission timestamp. They
  // differ whenever somebody fills this in the next morning, and the session
  // date is the one to sort the timeline by.
  form.addDateItem()
    .setTitle('Session date')
    .setHelpText('The meeting this note is about, not necessarily today.')
    .setRequired(true);

  // 2. Who, by slot rather than name.
  form.addListItem()
    .setTitle('Who is writing this?')
    .setChoiceValues(['Kid 1', 'Kid 2', 'Kid 3', 'Kid 4', 'Kid 5', 'Coach'])
    .setRequired(true);

  // 3. Area, so the sheet can be filtered when filling in a prep sheet.
  form.addCheckboxItem()
    .setTitle('Area')
    .setHelpText('Tick everything this note touches.')
    .setChoiceValues([
      'Robot',
      'Programming',
      'Innovation Project',
      'Core Values',
      'Other'
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What we did, built, or changed')
    .setHelpText(
      'Even a small change counts. Taking something apart and putting it back ' +
      'differently is an iteration.'
    );

  form.addParagraphTextItem()
    .setTitle('What broke or did not work, and why we think so')
    .setHelpText(
      'Worth more to judges than what worked. "This is version four and one to ' +
      'three failed because..." is the strongest thing you can say.'
    );

  form.addTextItem()
    .setTitle('Numbers from testing')
    .setHelpText(
      'Attempts, successes, distances, speeds. "Four out of ten, then nine out ' +
      'of ten after gyro correction" beats "it got better".'
    );

  form.addParagraphTextItem()
    .setTitle('Anyone we talked to, and what they told us')
    .setHelpText(
      'Especially anything that surprised you or changed your mind, and what ' +
      'you did differently as a result.'
    );

  form.addParagraphTextItem()
    .setTitle('A Core Values moment')
    .setHelpText(
      'Something small is fine. Somebody helped somebody, something was funny, ' +
      'somebody stuck with something hard.'
    );

  form.addParagraphTextItem()
    .setTitle('Any disagreement, and how we sorted it out')
    .setHelpText(
      'Judges ask about this almost every year, and "we never disagree" is a ' +
      'worse answer than a real story.'
    );

  form.addParagraphTextItem()
    .setTitle('What I personally did today')
    .setHelpText(
      'Answer for yourself, not the team. Judges pick who they ask.'
    );

  form.addTextItem()
    .setTitle('What needs photographing before it changes')
    .setHelpText(
      'You can only photograph version one before you take it apart. After ' +
      'that it is gone.'
    );

  form.addParagraphTextItem()
    .setTitle('Anything else')
    .setHelpText('Questions, worries, ideas, things to ask the coach.');

  var published = form.getPublishedUrl();

  Logger.log('--- Paste this into the iframe in docs/after-class-notes.md ---');
  Logger.log('EMBED URL: ' + published + '?embedded=true');
  Logger.log('');
  Logger.log('--- For docs/team-links.md (kept off the public site) ---');
  Logger.log('Form (public, it is embedded on the site): ' + published);
  Logger.log('Edit the form: ' + form.getEditUrl());
  Logger.log('');
  Logger.log('Next: check the form is published with responder access set to');
  Logger.log('"Anyone with the link", then Responses tab > Sheets icon to');
  Logger.log('create the linked spreadsheet.');
}
