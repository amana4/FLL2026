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
// gyroscope has its own part, Sensors, and the last part is Iteration and team.
var ROLE_SLOT = {'Strategy': 'Kid 5', 'Robot': 'Kid 2', 'Code': 'Kid 1',
                 'Sensors': 'Kid 3', 'Iteration and team': 'Kid 4'};

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
      'Reaching Roots, then the Drone Survey and Biocentric Architecture. That run ' +
      'is one straight push and back, so it hardly ever goes wrong.',
      'Then comes what we call the robo taxi. Our attachments and the keystone ' +
      'species wait on the left. The robot carries one attachment and the keystone ' +
      'species across to the right. That one attachment does several missions ' +
      'there, so we don\'t stop to swap.',
      'We skipped Lucky Leaves. It\'s far away, partly luck, and only 10 or 20 ' +
      'points. Now ROBOT will show you the robot.'
    ],
    check: ['Points and seconds for each run, from the scoresheet and a stopwatch',
            'How many times out of 10 Phase 2 works'],
    cue: ['Time is our biggest limit', 'Close missions first', 'Phase 2: one straight push and back', 'Robo taxi: attachment and keystone to the right', 'Skipped Lucky Leaves: far, luck, 10 or 20 points']
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
    cue: ['Six designs: blue wheels slip', 'Flat: lines up on walls and mat lines', '6 ports: 2 wheels, 2 attachments, 2 colour sensors', 'Gravity mounting: one move (do the swap)', 'Push before motors. Arm starts on the stopper']
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
      'spinning off the table. Now SENSORS will tell you about our sensors.'
    ],
    check: ['What changed in drive_cm from last year: the wheel size, 88 mm to 62.4 mm'],
    cue: ['Python: we reused last year\'s drive_cm', 'Changed the wheel size, 88 mm to 62.4 mm', 'Layers: the run says what, the library says how', '45 degrees off: it stops']
  },
  {
    role: 'Sensors', time: '3:00 to 4:00', rows: 'CREATE: code and sensors',
    show: 'The gyro steps picture, and the gyro loop.',
    script: [
      'We only use the gyroscope to steer. Our hub has two colour sensors plugged ' +
      'in, but we don\'t use them. The gyroscope works anywhere on the mat, not ' +
      'just near a line.',
      'The gyroscope measures yaw. Yaw is the direction the robot is pointing, like ' +
      'a compass. We use it in three steps. One: at the start of every mission we ' +
      'zero the yaw, so the way the robot points becomes zero. Two: we turn with ' +
      'the gyroscope. face 90 always means 90 degrees from the start, so small ' +
      'mistakes don\'t add up. Three: while it drives, it checks the yaw every 15 ' +
      'milliseconds. If the robot drifts 5 degrees left, it steers back right, ' +
      'harder the further off it is. Now ITERATION will tell you how we test, and ' +
      'about our team.'
    ],
    check: ['The 5-degree example: drift 5 left, error -5, it steers back right',
            'Why the gyroscope and not the colour sensors'],
    cue: ['Only the gyroscope steers', 'Colour sensors: plugged in, not used', 'Yaw = the way the robot points', '1 zero, 2 turn, 3 drive straight', 'Drifts 5 left: steers back right']
  },
  {
    role: 'Iteration and team', time: '4:00 to 5:00',
    rows: 'ITERATE: testing and improvements. DESIGN and COMMUNICATE: team',
    show: 'The printed run log table, then the who-did-what page.',
    script: [
      'We test each run ten times and write down how many work. (Say a real ' +
      'number.) Here\'s one fix. Our arm was sometimes too high and sometimes too ' +
      'low. We printed where the motor was after every move, and found the arm ' +
      'wasn\'t starting in the same place. Two ideas failed. The one that worked: ' +
      'the arm starts on its stopper every time, and the code counts from there. ' +
      'We learned to measure first, then fix.',
      'All five of us built something and coded something. (Each person says one ' +
      'sentence: "I built ... and I coded ...") We\'re most proud of ... Thank you. ' +
      'Ask any of us anything.'
    ],
    check: ['The 10-run result for every run, with dates',
            'One "I built ... and I coded ..." line from every member'],
    cue: ['10 runs each: say the real number', 'Arm fix: measured, 2 ideas failed, stopper works', 'Measure first, then fix', 'Everyone: I built ... I coded ...', 'Proud of ... Ask any of us anything']
  }
];

// The 32 judge questions, from section 7 of robot-design/exceeds-prep.md.
// Each: [part, number, question, a strong answer, a harder follow-up].
var QUESTIONS = [
  ['Robot', 1, 'Why is your robot shaped like that?',
   'A flat box squares up on a wall, so every run starts the same way.',
   'What if it starts crooked?'],
  ['Robot', 2, 'Why those wheels?',
   'The designs that slipped all used blue SPIKE wheels, so we use grippy ones.',
   'How did you check yours don\'t slip?'],
  ['Robot', 3, 'Where is the robot\'s weight?',
   'Team to measure: say where the heaviest part is, and that you checked for a wobble.',
   'How did you test it?'],
  ['Robot', 4, 'How does the BOXOR frame move the arm?',
   'Two bevel gears turn the movement through 90 degrees.',
   'What is the gear ratio?'],
  ['Robot', 5, 'Why gravity mounting?',
   'One move to swap. Last season, swaps were slow.',
   'Has one ever fallen off?'],
  ['Robot', 6, 'How long does a swap take?',
   'Give the measured time.',
   'How did you measure it?'],
  ['Robot', 7, 'Why a push instead of a motor?',
   'Motors can go wrong. A push can\'t.',
   'When did you need a motor anyway?'],
  ['Robot', 8, 'Why is the attachment on the back?',
   'Team to agree.',
   'Why do your distances have minus signs?'],
  ['Robot', 9, 'What would you change with more time?',
   'Take the play out of the arm gears, maybe with a rubber band.',
   'How would you know it worked?'],
  ['Strategy', 10, 'What is the robo taxi?',
   'One trip carries the attachment and the keystone to the right.',
   'What if the keystone falls off?'],
  ['Sensors', 11, 'How does it drive straight?',
   'It reads the gyro every 15 ms and steers back, harder the further off.',
   'What stops it wiggling?'],
  ['Code', 12, 'Why Python?',
   'Last year\'s Python, more control, and git shows every change.',
   'What was hard about switching?'],
  ['Sensors', 13, 'What does face(90) do?',
   'Turns to point 90 degrees from where we started.',
   'Why not just turn 90?'],
  ['Sensors', 14, 'What is PID?',
   'P pushes harder when far off, I pushes more when stuck, D eases off when closing in fast.',
   'Which parts does drive_cm use?'],
  ['Sensors', 15, 'Why not the colour sensors?',
   'They\'re plugged in, but only the gyroscope steers. It works everywhere on the mat, not just near a line.',
   'Would a sensor have helped anywhere?'],
  ['Code', 16, 'What if something goes wrong in a run?',
   'More than 45 degrees off, it stops. Over 8 seconds, it gives up and goes on.',
   'Why stop?'],
  ['Code', 17, 'How are distances accurate?',
   'We asked for 180 cm and got 179, so we scale by 179/180.',
   'What if you change the wheels?'],
  ['Code', 18, 'What did you reuse from last year?',
   'drive_cm. We changed the wheel size from 88 mm to 62.4 mm.',
   'Why did that number matter?'],
  ['Robot', 19, 'How does the arm know where it is?',
   'It starts on its stopper, and the code calls that zero.',
   'What if it doesn\'t start there?'],
  ['Code', 20, 'What\'s the cleverest thing in your code?',
   'The arm lifts while the robot drives home, by leaving out await.',
   'How much time does it save?'],
  ['Strategy', 21, 'Why this order of runs?',
   'Left first, close first, then the robo taxi.',
   'What if the first run fails?'],
  ['Strategy', 22, 'Which mission did you skip?',
   'Lucky Leaves: far, partly luck, 10 or 20 points.',
   'What would make it worth doing?'],
  ['Iteration and team', 23, 'How reliable is your robot?',
   'Give the 10-run numbers.',
   'Which run is weakest?'],
  ['Iteration and team', 24, 'How do you test a change?',
   'Change one thing, run it 10 times, compare.',
   'Give an example.'],
  ['Iteration and team', 25, 'What broke, and how did you fix it?',
   'One fix story, four parts: problem, how we found out, what we changed, result.',
   'How did you find the cause?'],
  ['Iteration and team', 26, 'What didn\'t work?',
   'Pushing the arm into its stopper lifted the attachment, so we dropped that idea.',
   'What did you do instead?'],
  ['Iteration and team', 27, 'How do you know a fix helped?',
   'A number before and a number after.',
   'What if it only helped sometimes?'],
  ['Iteration and team', 28, 'Who built and coded what?',
   'Each member answers for themselves.',
   'Explain your teammate\'s part.'],
  ['Iteration and team', 29, 'How did you share the work?',
   'Roles, and we swapped so everyone tried each.',
   'What happened when you disagreed?'],
  ['Strategy', 30, 'Whose idea was the robo taxi?',
   'The true answer.',
   'How did the team decide?'],
  ['Iteration and team', 31, 'What did you learn?',
   'One real lesson each.',
   'How will you use it next season?'],
  ['Iteration and team', 32, 'What are you most proud of?',
   'Said like you mean it.',
   'Why that one?']
];

// The handover names in the scripts, in capitals above, become first names.
function fillNames(text) {
  return text.replace(/\bROBOT\b/g, who('Robot'))
             .replace(/\bCODE\b/g, who('Code'))
             .replace(/\bSENSORS\b/g, who('Sensors'))
             .replace(/\bITERATION\b/g, who('Iteration and team'));
}

function createScriptDoc() {
  var doc = DocumentApp.create('FLL BIOGLOW: Robot Design presentation scripts');
  var body = doc.getBody();
  var H = DocumentApp.ParagraphHeading;

  // Print-friendly: normal margins (in points, 72 to an inch), 11 pt text, and
  // each speaker's part starts on a new page and fits on one page.
  body.setMarginTop(50).setMarginBottom(50).setMarginLeft(60).setMarginRight(60);
  var style = {};
  style[DocumentApp.Attribute.FONT_FAMILY] = 'Arial';
  style[DocumentApp.Attribute.FONT_SIZE] = 11;
  body.setAttributes(style);

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
      body.appendParagraph(fillNames(para)).setItalic(true).editAsText().setFontSize(11);
    });

    body.appendParagraph('My script, in my own words').setHeading(H.HEADING2);
    var box = body.appendTable([['Write here.']]);
    box.setBorderWidth(1);
    box.getCell(0, 0).setBackgroundColor('#fdf1ea').setPaddingTop(6)
       .setPaddingBottom(40);

    body.appendParagraph('Facts to check before we practise').setHeading(H.HEADING2);
    p.check.forEach(function (c) { body.appendListItem('☐ ' + c); });

    body.appendParagraph('Questions a judge might ask me').setHeading(H.HEADING2);
    QUESTIONS.filter(function (q) { return q[0] === p.role; }).forEach(function (q) {
      var para = body.appendParagraph(q[1] + '. ' + q[2]);
      para.editAsText().setBold(true);
      body.appendParagraph('Strong answer: ' + q[3]).editAsText().setBold(false);
      body.appendParagraph('Follow-up: ' + q[4]).editAsText().setBold(false)
          .setItalic(true);
    });

    body.appendParagraph('Time it').setHeading(H.HEADING2);
    body.appendTable([['Practice', 'Time taken', 'What to cut or fix'],
                      ['1', '', ''], ['2', '', ''], ['3', '', '']]);

    // A cue card to cut out and hold: the key points only, in big type.
    body.appendParagraph('Cue card: cut out and hold').setHeading(H.HEADING2);
    var card = body.appendTable([[who(p.role) + ': ' + p.role + '\n\n' +
      p.cue.map(function (c) { return '• ' + c; }).join('\n')]]);
    card.setBorderWidth(2).setBorderColor('#16362b');
    card.getCell(0, 0).setPaddingTop(8).setPaddingBottom(8).setPaddingLeft(10)
        .editAsText().setFontSize(13).setBold(true);
  });

  // The drill sheet: every question, no answers, for the coach to read out.
  body.appendPageBreak();
  body.appendParagraph('Question drill: all 32').setHeading(H.HEADING1);
  body.appendParagraph('The coach reads a question and points at anyone. Answer in ' +
    'two or three sentences, then stop. "I don\'t know, but my teammate built ' +
    'that" is a good answer.');
  var drill = [['#', 'Question', 'Part']];
  QUESTIONS.forEach(function (q) { drill.push([String(q[1]), q[2], q[0]]); });
  body.appendTable(drill);

  doc.saveAndClose();
  Logger.log('--- For docs/team-links.md (kept off the public site) ---');
  Logger.log('Presentation scripts doc: ' + doc.getUrl());
  Logger.log('Next: Share > add the team as Editors.');
}
