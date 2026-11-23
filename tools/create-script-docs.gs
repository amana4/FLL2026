/**
 * Creates the Google Doc the team uses to write the five-minute Robot Design
 * explanation: one shared doc, one section per speaker, each with a starter
 * script to rewrite in their own words.
 *
 * The starter scripts are the same as section 6 of robot-design/exceeds-prep.md
 * ("Going for Exceeds"). If you change a script there, change it here too.
 *
 * This is Google Apps Script, not part of the website build. It is the same
 * pattern as tools/create-robot-design-test-form.gs.
 *
 * HOW TO RUN
 *   1. Go to https://script.google.com and click "New project".
 *   2. Delete the sample code, paste this whole file in, and save.
 *   3. Fill in NAMES below with first names. Do not commit real names to this
 *      file: the repo is public. The Google Doc itself stays in your Drive.
 *   4. Pick "createScriptDoc" in the function dropdown and click Run.
 *   5. Google asks you to authorise it the first time. That prompt is for your
 *      own account creating your own document; it is expected.
 *   6. Open "Execution log" and copy the link into docs/team-links.md.
 *   7. Share the doc with the team: Share > the kids' or parents' addresses,
 *      as Editor.
 *
 * The guide links point at the public website, so they work only after the
 * Going for Exceeds page and the workshop slides are pushed to main.
 */

// Who is in which slot, from docs/team-roster.md. Fill in first names in your
// pasted copy before running. Keep the Kid labels here: this file is public.
var NAMES = {'Kid 1': 'Kid 1', 'Kid 2': 'Kid 2', 'Kid 3': 'Kid 3',
             'Kid 4': 'Kid 4', 'Kid 5': 'Kid 5'};

// Who leads which part, by roster slot. Testing is the ITERATE part. The same
// as ROLE_SLOT in tools/make-exceeds-pptx.py. Changed 22 November 2026: the
// gyroscope moved from Code to the last part, Sensors and team.
var ROLE_SLOT = {'Strategy': 'Kid 5', 'Robot': 'Kid 2', 'Code': 'Kid 1',
                 'Testing': 'Kid 4', 'Sensors and team': 'Kid 3'};

var SITE = 'https://amana4.github.io/FLL2026/robot-design/';
var LINKS = [
  ['Going for Exceeds (the full guide)', SITE + 'exceeds-prep/'],
  ['Our key facts (read this first)', SITE + 'exceeds-prep/#our-key-facts'],
  ['The workshop slides', SITE + 'exceeds-workshop.html'],
  ['The mission map', SITE + 'diagrams/mission-route.svg'],
  ['Presentation and Q&A', SITE + 'presentation/']
];

function who(role) { return NAMES[ROLE_SLOT[role]]; }

var PARTS = [
  {
    role: 'Strategy', time: '0:00 to 1:10', rows: 'IDENTIFY: mission strategy',
    show: 'Point at the mission map.',
    script: [
      'Hello, we\'re the Bumble Bots. In the Robot Game we have two and a half ' +
      'minutes, so our biggest limit is time. Almost every choice we made was to ' +
      'save time.',
      'First, we do the missions close to our home first. Short trips are quicker ' +
      'and more reliable. Our first runs do Flip the Rock and Exploding Seeds, then ' +
      'the Drone Survey and Biocentric Architecture. That run is one straight push ' +
      'and back, so it hardly ever goes wrong.',
      'Then comes what we call the robo taxi. Our attachments and the keystone ' +
      'species wait on the left. The robot does Reaching Roots on the way, then ' +
      'carries one attachment and the keystone species across to the right. That ' +
      'one attachment does several missions there, so we don\'t stop to swap.',
      'We skipped Lucky Leaves. It\'s far away, partly luck, and only 10 or 20 ' +
      'points. Now ROBOT will show you the robot.'
    ],
    check: ['Points and seconds for each run, from the scoresheet and a stopwatch',
            'How many times out of 10 phase2 works'],
    questions: ['Why these missions?', 'Why that order?',
                'What would you add with more time?']
  },
  {
    role: 'Robot', time: '1:10 to 2:15', rows: 'CREATE: attachments. IDENTIFY: resources',
    show: 'Do a live attachment swap. Hold up an old attachment next to the new one.',
    script: [
      'Before we built anything, we compared six robot designs. The three that ' +
      'slipped all had blue SPIKE wheels, so we chose grippy wheels.',
      'Our robot is flat, with straight walls. It lines up against the wall and ' +
      'with the lines on the mat, so every run starts straight. The hub has six ' +
      'ports: two for the wheels, two for the attachment motors and two for colour ' +
      'sensors.',
      'To change attachments fast we use gravity. Pegs line the attachment up, and ' +
      'its own weight holds it. Last season, changing attachments took a long time. ' +
      'Now it\'s one move. (Do the swap.)',
      'Where we can, we use simple push and pull attachments instead of a motor. A ' +
      'motor can go wrong, but a push can\'t. When we do use a motor arm, it always ' +
      'starts on a stopper, so it starts from the same fixed point every time. ' +
      'Next, CODE will explain our code.'
    ],
    check: ['How many seconds a swap takes, timed 5 times',
            'What we changed from the BOXOR design'],
    questions: ['Why gravity mounting?', 'Has an attachment ever fallen off?',
                'Why push instead of a motor?']
  },
  {
    role: 'Code', time: '2:15 to 3:00', rows: 'CREATE: code',
    show: 'One function on paper or a laptop, and the code layers picture.',
    script: [
      'We code in Python. Last year\'s team left us Python, so we could reuse it. ' +
      'Our drive command, drive_cm, is from last year. We only changed the wheel ' +
      'size. Python also gives us more control over every number.',
      'Our code is in layers. Each run says what to do, like drive 44 centimetres ' +
      'and face 90. Our library says how: speed up gently, steer, and stop on the ' +
      'mark. If the robot ever gets 45 degrees off course, it stops instead of ' +
      'spinning off the table. Now TESTING will tell you how we test.'
    ],
    check: ['What changed in drive_cm from last year: the wheel size, 88 mm to 62.4 mm'],
    questions: ['Why Python?', 'What does your library do?',
                'What happens if something goes wrong?']
  },
  {
    role: 'Testing', time: '3:00 to 4:00', rows: 'ITERATE: testing and improvements',
    show: 'The printed run log table.',
    script: [
      'We test each run ten times and write down how many work. (Say a real ' +
      'number.)',
      'Here\'s one fix. The arm in one run was sometimes too high and sometimes too ' +
      'low. We printed where the motor was after every move. That showed the arm ' +
      'wasn\'t starting in the same place: two runs started 45 degrees apart.',
      'Our first idea worked until we took the attachment off and put it back. Our ' +
      'second idea, pushing the arm into its stopper, lifted the attachment off. So ' +
      'we used the simplest answer: the arm starts on its stopper every time, and ' +
      'the code counts from there. Now it works even after we put the attachment ' +
      'back on. We learned to measure first, then fix. Now SENSORS will tell you ' +
      'about our sensors and our team.'
    ],
    check: ['The 10-run result for every run, with dates'],
    questions: ['How do you know it is reliable?', 'What didn\'t work?',
                'How did you find the cause?']
  },
  {
    role: 'Sensors and team', time: '4:00 to 5:00',
    rows: 'CREATE: sensors. DESIGN: everyone. COMMUNICATE: lessons and pride',
    show: 'The gyro steps picture, then the who-did-what page.',
    script: [
      'We only use the gyroscope to steer. Our two colour sensors are plugged in, ' +
      'but we don\'t use them. The gyroscope measures yaw: the way the robot ' +
      'points, like a compass. We use it in three steps. Zero the yaw at the start, ' +
      'turn with the gyroscope, and check the yaw every 15 milliseconds to drive ' +
      'straight.',
      'All five of us built something and coded something. (Each person says one ' +
      'sentence: "I built ... and I coded ...") We\'re most proud of ... Thank you. ' +
      'Ask any of us anything.'
    ],
    check: ['The 5-degree example: drift 5 left, error -5, it steers back right',
            'One "I built ... and I coded ..." line from every member'],
    questions: ['Why not the colour sensors?', 'What is yaw?',
                'What are you most proud of?']
  }
];

// The handover names in the scripts, in capitals above, become first names.
function fillNames(text) {
  return text.replace(/\bROBOT\b/g, who('Robot'))
             .replace(/\bCODE\b/g, who('Code'))
             .replace(/\bTESTING\b/g, who('Testing'))
             .replace(/\bSENSORS\b/g, who('Sensors and team'));
}

function createScriptDoc() {
  var doc = DocumentApp.create('FLL BIOGLOW: Robot Design presentation scripts');
  var body = doc.getBody();
  var H = DocumentApp.ParagraphHeading;

  body.appendParagraph('Robot Design presentation scripts').setHeading(H.TITLE);
  body.appendParagraph(
    'We have 5 minutes to explain our robot, then 5 minutes of questions. Each of ' +
    'us has about one minute. Your starter script is below. Rewrite it in your own ' +
    'words in the box under it. Say it out loud with a timer, and cut what runs ' +
    'long. Do not learn it word for word: know the points, and say them your way.');

  body.appendParagraph('Use these as your guide').setHeading(H.HEADING2);
  LINKS.forEach(function (l) {
    body.appendListItem(l[0]).setLinkUrl(l[1]);
  });

  body.appendParagraph('Running order').setHeading(H.HEADING2);
  var rows = [['Time', 'Who', 'Part']];
  PARTS.forEach(function (p) { rows.push([p.time, who(p.role), p.role]); });
  body.appendTable(rows);

  PARTS.forEach(function (p) {
    body.appendPageBreak();
    body.appendParagraph(who(p.role) + ': ' + p.role + ' (' + p.time + ')')
        .setHeading(H.HEADING1);
    body.appendParagraph('Rubric lines: ' + p.rows);
    body.appendParagraph('Show: ' + p.show);

    body.appendParagraph('Starter script').setHeading(H.HEADING2);
    p.script.forEach(function (para) {
      body.appendParagraph(fillNames(para)).setItalic(true);
    });

    body.appendParagraph('My script, in my own words').setHeading(H.HEADING2);
    var box = body.appendTable([['Write here.']]);
    box.setBorderWidth(1);
    box.getCell(0, 0).setBackgroundColor('#fdf1ea').setPaddingTop(8)
       .setPaddingBottom(60);

    body.appendParagraph('Facts to check before we practise').setHeading(H.HEADING2);
    p.check.forEach(function (c) { body.appendListItem('☐ ' + c); });

    body.appendParagraph('Questions a judge might ask me').setHeading(H.HEADING2);
    p.questions.forEach(function (q) { body.appendListItem(q); });

    body.appendParagraph('Time it').setHeading(H.HEADING2);
    body.appendTable([['Practice', 'Time taken', 'What to cut or fix'],
                      ['1', '', ''], ['2', '', ''], ['3', '', '']]);
  });

  doc.saveAndClose();
  Logger.log('--- For docs/team-links.md (kept off the public site) ---');
  Logger.log('Presentation scripts doc: ' + doc.getUrl());
  Logger.log('Next: Share > add the team as Editors.');
}
