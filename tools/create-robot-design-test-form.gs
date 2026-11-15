/**
 * Creates the Robot Design test form in one run: a marked quiz, then open
 * questions. It matches robot-design/robot-design-test.md and
 * robot-design/our-robot-explained.md. If you change a question here, change
 * those pages too.
 *
 * This is Google Apps Script, not part of the website build. It is the same
 * pattern as tools/create-notes-form.gs.
 *
 * HOW TO RUN
 *   1. Go to https://script.google.com and click "New project".
 *   2. Delete the sample code, paste this whole file in, and save.
 *   3. Fill in TEAM_NAMES below.
 *   4. Pick "createRobotDesignTestForm" in the function dropdown and click Run.
 *   5. Google asks you to authorise it the first time. That prompt is for your
 *      own account creating your own form; it is expected.
 *   6. Open "Execution log" and copy the EMBED URL it prints.
 *
 * AFTERWARDS, in the Forms UI:
 *   - Check the form is published and that responder access is "Anyone with the
 *     link". A script-created form may start unpublished, and then nobody can
 *     submit.
 *   - Settings > Quizzes. Set "Release marks" to "Immediately after each
 *     submission". Under "Respondent can see", turn on "Missed questions" and
 *     "Point values". Leave "Correct answers" off, so a retake still means
 *     going back to the page.
 *   - Responses tab, Sheets icon, to create the linked spreadsheet.
 *
 * NAMES
 * The 15 August 2026 decision to show first names covers the after-class notes
 * form only. This form is also embedded on the public site, so the coach
 * decides whether it gets first names or the Kid 1 to Kid 5 labels. Either
 * way, do not commit real names to this file: anything in git history stays
 * there, but a form field can be changed in seconds.
 */

// Fill these in before running. Order does not matter.
var TEAM_NAMES = ['Kid 1', 'Kid 2', 'Kid 3', 'Kid 4', 'Kid 5'];

var PAGE = 'Our Robot, Explained';

// Part 1. Each question: title, choices with the RIGHT ONE FIRST, the section
// of the knowledge base that has the answer, and why it is right. The script
// moves the right choice to a different place in each question, so "always
// pick the first one" does not work.
var QUIZ = [
  {
    title: 'Which sockets are the drive motors plugged into, in our final code?',
    choices: ['F (left) and A (right)', 'A (left) and B (right)',
              'C (left) and D (right)', 'E (left) and F (right)'],
    section: 1,
    why: 'F is left and A is right. On 20 September the robot stopped with ' +
         'ENODEV until the code used F and A.'
  },
  {
    title: 'What does face(90) do?',
    choices: [
      'Turns until the robot points 90 degrees away from the way it pointed ' +
        'when the program started in base',
      'Turns 90 more degrees from wherever the robot points now',
      'Drives 90 cm',
      'Lifts the attachment 90 degrees'
    ],
    section: 3,
    why: 'face always measures from base, the way the robot pointed at the start.'
  },
  {
    title: 'Why do we use face instead of "turn by 90 degrees"?',
    choices: [
      'A small mistake in one turn does not get passed on to the next turn',
      'It is shorter to type',
      'It does not need the gyro',
      'The rules say we must'
    ],
    section: 3,
    why: 'Four turns round a square end about 1 degree out with face, ' +
         'instead of 17.'
  },
  {
    title: 'Why did we delete the old turn that only counted wheel rotations?',
    choices: [
      'It was slower and less accurate than the gyro turn',
      'It broke a motor',
      'The rules do not allow it',
      'It could only turn left'
    ],
    section: 3,
    why: '1.54 seconds and 4.26 degrees out, against 1.18 seconds and ' +
         '0.58 degrees for the gyro turn.'
  },
  {
    title: 'What does YAW_SIGN = -1 tell the code?',
    choices: [
      'Which way the gyro counts when the robot turns',
      'That the robot drives backwards',
      'That the left motor is plugged in the wrong way round',
      'How fast the robot turns'
    ],
    section: 3,
    why: 'Our gyro counts up when the robot turns anticlockwise. We found ' +
         'out when drive_cm(-44) spun on the spot.'
  },
  {
    title: 'What does our robot use to find its way around the field?',
    choices: [
      'The gyro and the motor encoders',
      'The two colour sensors, following the black lines',
      'A distance sensor',
      'Only a timer'
    ],
    section: 1,
    why: 'The team stopped using the colour sensors on 20 September 2026.'
  },
  {
    title: 'Why do most programs have set_calibration_scale(179/180)?',
    choices: [
      'On our mat the robot drove 179 cm when asked for 180, so every ' +
        'distance is adjusted to match',
      'The robot is 179 mm long',
      'The gyro is 1 degree out',
      'It saves battery'
    ],
    section: 3,
    why: 'Calibration means measuring the real robot and adjusting the code ' +
         'to match.'
  },
  {
    title: 'How far does drive_cm(30) drive?',
    choices: ['30 cm', '30 mm', '300 cm', '3 cm'],
    section: 3,
    why: 'Python uses centimetres. The Word Blocks used millimetres, so ' +
         '.Forward 300 in blocks is drive_cm(30).'
  },
  {
    title: 'What does the bevel gear pair in the BOXOR frame do?',
    choices: [
      'Turns the movement through 90 degrees, so the motor can swing an arm',
      'Makes the robot drive straighter',
      'Holds the attachment on the robot',
      'Measures how far the arm moved'
    ],
    section: 2,
    why: 'Bevel gears meet at a right angle, so the movement changes ' +
         'direction by 90 degrees.'
  },
  {
    title: 'In phase0-alt.py, why does the robot run face(0) straight after ' +
           'backing into the rock?',
    choices: [
      'Hitting the rock knocks the robot crooked, so it straightens up ' +
        'before it drives on',
      'To point at M13 Keystone Species',
      'To reset the gyro to zero',
      'To wait for the attachment to finish'
    ],
    section: 5,
    why: 'The comment says "Straighten post collision before backing off for ' +
         'accuracy". A test found a problem, and the code changed: that is ' +
         'ITERATE.'
  },
  {
    title: 'Which rubric row asks for "clear evidence of repeated testing of ' +
           'their robot and code"?',
    choices: ['ITERATE', 'IDENTIFY', 'CREATE', 'COMMUNICATE'],
    section: 0,
    why: 'ITERATE: test, find a problem, change something, test again.'
  },
  {
    title: 'Some Robot Design rubric lines also count toward which other award?',
    choices: ['Core Values', 'Innovation Project', 'Robot Performance',
              'Engineering Excellence'],
    section: 0,
    why: 'On the rubric they have a gear-shaped box. Core Values make up ' +
         '25% of the Champion\'s score.'
  }
];

// Part 2. Open questions, not marked. Grouped by rubric row.
var OPEN = [
  ['IDENTIFY: Which missions does our robot try, and why those?', ''],
  ['IDENTIFY: Name one mission we skipped, and the reason.',
   'Points, time, or risk. "It was worth 10 points but took 40 seconds" ' +
   'beats "it was too hard".'],
  ['IDENTIFY: Where did we get help or ideas?',
   'For example videos, other teams, building instructions, or coaches.'],
  ['DESIGN: What did you personally build, and what did you code?',
   'Answer for yourself, not the team. Judges pick who they ask.'],
  ['DESIGN: How did the team share out the work?', ''],
  ['CREATE: Pick one attachment. What does it do, and what did we change ' +
   'from the original design?', ''],
  ['CREATE: Why did we stop using the colour sensors, and what do we use to ' +
   'steer instead?', ''],
  ['CREATE: Phase 5.py does four jobs: "Pull", "open door", "ant" and ' +
   '"Tree support". Which mission number is each one?', ''],
  ['ITERATE: Name something that broke or did not work. What did we change, ' +
   'and what happened after?', ''],
  ['ITERATE: How do we know a run is reliable?',
   'Give a number if you know one, for example "8 out of 10".'],
  ['COMMUNICATE: Explain our robot to a judge in three sentences.', ''],
  ['COMMUNICATE: What are you most proud of?', ''],
  ['What do you not know yet, that we should sort out in class?',
   '"I don\'t know" is a good answer if it is true.']
];

function sectionName(n) {
  return n === 0 ? 'the rubric table at the top of ' + PAGE
                 : 'section ' + n + ' of ' + PAGE;
}

function createRobotDesignTestForm() {
  var form = FormApp.create('FLL BIOGLOW: Robot Design test');

  form.setDescription(
    'Read "' + PAGE + '" first and keep it open. Looking things up is allowed. ' +
    'Part 1 is marked as soon as you submit, and you can take it again as ' +
    'many times as you like. Part 2 has no right answers: write what you ' +
    'would say to a judge.'
  );

  form.setIsQuiz(true);
  // No email collection, so no login is needed, and no children's addresses
  // end up in the sheet. Same reasoning as the after-class notes form.
  form.setCollectEmail(false);
  form.setAllowResponseEdits(true);
  form.setLimitOneResponsePerUser(false);
  form.setShowLinkToRespondAgain(true);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    'Done. Press "View score" to see Part 1. If you missed one, read the hint, ' +
    'go back to the page, and try again.'
  );

  form.addListItem()
    .setTitle('Who is writing this?')
    .setChoiceValues(TEAM_NAMES.concat(['Coach']))
    .setRequired(true);

  form.addSectionHeaderItem()
    .setTitle('Part 1: Quick quiz')
    .setHelpText('One point each.');

  QUIZ.forEach(function (q, n) {
    // Rotate so the right choice lands at position n % 4.
    var k = n % q.choices.length;
    var right = q.choices[0];
    var order = q.choices.slice(q.choices.length - k)
      .concat(q.choices.slice(0, q.choices.length - k));
    var item = form.addMultipleChoiceItem();
    item.setTitle(q.title)
      .setChoices(order.map(function (text) {
        return item.createChoice(text, text === right);
      }))
      .setPoints(1)
      .setRequired(true)
      .setFeedbackForCorrect(
        FormApp.createFeedback().setText('Right. ' + q.why).build())
      .setFeedbackForIncorrect(
        FormApp.createFeedback()
          .setText('Not quite. Read ' + sectionName(q.section) + ' again.')
          .build());
  });

  form.addPageBreakItem()
    .setTitle('Part 2: Explain it')
    .setHelpText(
      'No marks and no right answers. Write in your own words, the way you ' +
      'would say it to a judge. Short is fine. Skip any you cannot answer.'
    );

  OPEN.forEach(function (q) {
    var item = form.addParagraphTextItem().setTitle(q[0]);
    if (q[1]) item.setHelpText(q[1]);
  });

  var published = form.getPublishedUrl();

  Logger.log('--- Paste this into robot-design/robot-design-test.md ---');
  Logger.log('EMBED URL: ' + published + '?embedded=true');
  Logger.log('');
  Logger.log('--- For docs/team-links.md (kept off the public site) ---');
  Logger.log('Form (public, it is embedded on the site): ' + published);
  Logger.log('Edit the form: ' + form.getEditUrl());
  Logger.log('');
  Logger.log('Next: publish the form, set the quiz settings listed at the top');
  Logger.log('of this script, then Responses tab > Sheets icon.');
}
