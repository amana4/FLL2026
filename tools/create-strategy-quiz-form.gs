/**
 * Creates the "Strategy and design" quiz as a Google Form: a marked quiz in
 * three parts, then open questions. Every answer comes from the "Our key facts"
 * section of robot-design/exceeds-prep.md. If you change a fact there, change
 * the question here too.
 *
 * This is Google Apps Script, not part of the website build. It is the same
 * pattern as tools/create-robot-design-test-form.gs.
 *
 * HOW TO RUN
 *   1. Go to https://script.google.com and click "New project".
 *   2. Delete the sample code, paste this whole file in, and save.
 *   3. Fill in TEAM_NAMES below. Do not commit real names to this file.
 *   4. Pick "createStrategyQuizForm" in the function dropdown and click Run.
 *   5. Google asks you to authorise it the first time. That prompt is for your
 *      own account creating your own form; it is expected.
 *   6. Open "Execution log" and copy the links it prints into
 *      docs/team-links.md, which is kept off the public site.
 *
 * AFTERWARDS, in the Forms UI:
 *   - Check the form is published and responder access is "Anyone with the
 *     link".
 *   - Settings > Quizzes. Set "Release marks" to "Immediately after each
 *     submission". Under "Respondent can see", turn on "Missed questions" and
 *     "Point values". Leave "Correct answers" off, so a retake still means
 *     going back to the page.
 *   - Responses tab, Sheets icon, to create the linked spreadsheet.
 */

// Fill these in before running. Order does not matter.
var TEAM_NAMES = ['Kid 1', 'Kid 2', 'Kid 3', 'Kid 4', 'Kid 5'];

var GUIDE = 'the "Our key facts" section of Going for Exceeds';
var GUIDE_URL = 'https://amana4.github.io/FLL2026/robot-design/exceeds-prep/#our-key-facts';

// Each question: title, choices with the RIGHT ONE FIRST, and why it is right.
// The script moves the right choice to a different place in each question.
var MISSION_QUIZ = [
  {
    title: 'What is the biggest limit on how many points we can score?',
    choices: ['Time: a match is only 2 minutes 30 seconds',
              'The number of motors on the hub',
              'How heavy the robot is',
              'The size of the mat'],
    why: 'Almost every choice we made was to save time.'
  },
  {
    title: 'Which missions do we do first?',
    choices: ['The ones closest to our home',
              'The ones worth the most points, wherever they are',
              'The ones furthest away, while the battery is full',
              'Whichever the referee picks'],
    why: 'Short trips are quicker and more reliable.'
  },
  {
    title: 'Why do we do several missions with the same attachment?',
    choices: ['We stop to swap attachments less often, which saves time',
              'The rules allow only one attachment',
              'It makes the robot lighter',
              'Attachments are expensive'],
    why: 'Every swap in base uses match time.'
  },
  {
    title: 'What is the robo taxi?',
    choices: ['A run that does a mission on the way across the mat and carries an ' +
                'attachment and the keystone species to the right side',
              'A second robot that carries the first one',
              'A run that only drives across the mat and back',
              'A remote-controlled robot'],
    why: 'phase3 does M05 Reaching Roots on the way, then carries the attachment ' +
         'and the keystone species to the right.'
  },
  {
    title: 'Why does the robot carry the keystone species across instead of ' +
           'making a separate trip?',
    choices: ['It saves a whole trip, and the keystone arrives with the robot that ' +
                'needs it',
              'The keystone species is too heavy to carry twice',
              'The rules say it must start on the robot',
              'The right home is too small'],
    why: 'One trip carries everything to the right side.'
  },
  {
    title: 'Where does the keystone species go, and how many points is M13 ' +
           'worth in the rulebook?',
    choices: ['On the Mine dock, 30 points',
              'On the City dock, 10 points',
              'On the Farm dock, 40 points',
              'In the left home, 20 points'],
    why: 'Robot Game Rulebook, Mission 13: on the restoration platform with the ' +
         'young trees raised scores 30.'
  },
  {
    title: 'Which missions does phase2 do, and why is it so reliable?',
    choices: ['M01 Drone Survey and M15 Biocentric Architecture, with one straight ' +
                'push and back',
              'M03 Flip the Rock and M02 Exploding Seeds, with lots of turns',
              'M13 Keystone Species, with the colour sensor',
              'M04 Lucky Leaves, with a motor arm'],
    why: 'One straight push and back has very little that can go wrong.'
  },
  {
    title: 'Why did we skip M04 Lucky Leaves?',
    choices: ['It is far away, partly luck, and only 10 or 20 points',
              'It was too hard',
              'The referee does not score it',
              'Our robot cannot drive that far'],
    why: 'A strong reason gives numbers, not "it was too hard".'
  }
];

var ROBOT_QUIZ = [
  {
    title: 'Why is our robot flat, with straight walls?',
    choices: ['It lines up against the field wall and with the lines on the mat, ' +
                'so every run starts straight',
              'It looks better',
              'Flat robots are faster',
              'The rules say robots must be flat'],
    why: 'A flat wall can only sit one way against another flat wall.'
  },
  {
    title: 'The hub has six ports. What is plugged into them?',
    choices: ['Two wheel motors, two attachment motors and two colour sensors',
              'Four wheel motors and two attachment motors',
              'Six attachment motors',
              'Two wheel motors and four colour sensors'],
    why: 'Wheels on F and A, attachments on C and E, and two colour sensors.'
  },
  {
    title: 'Why do we use push and pull attachments instead of a motor where we can?',
    choices: ['A motor can go wrong, but a push can not',
              'Motors are not allowed on attachments',
              'Pushing scores double points',
              'We only have one motor'],
    why: 'Simple attachments are more reliable.'
  },
  {
    title: 'What is gravity mounting?',
    choices: ['Pegs line the attachment up, and its own weight holds it on',
              'Clipping the attachment on with pins',
              'Taping the attachment to the robot',
              'Hanging the attachment underneath the robot'],
    why: 'On or off in one move.'
  },
  {
    title: 'Why did we choose gravity mounting?',
    choices: ['Last season, changing attachments took a long time. Now it is one move',
              'It makes the robot taller',
              'It stops the gyroscope drifting',
              'It is the only way LEGO fits together'],
    why: 'Match time spent swapping is time not scoring.'
  },
  {
    title: 'Why does a motor arm always start resting on its stopper?',
    choices: ['So it starts from the same fixed point, and every move ends in the ' +
                'same place',
              'So the motor stays cool',
              'So the arm is out of the way of the referee',
              'So the battery lasts longer'],
    why: 'A move counts from where the arm starts. Start in the same place, end ' +
         'in the same place.'
  }
];

var CODE_QUIZ = [
  {
    title: 'Why do we code in Python?',
    choices: ['We could reuse last year\'s Python code, and it gives us more control',
              'Word Blocks are not allowed',
              'Python makes the motors stronger',
              'The judges only score Python'],
    why: 'Last year\'s team left us Python, including drive_cm.'
  },
  {
    title: 'Our drive command, drive_cm, came from last year. What did we change?',
    choices: ['The wheel size, from 88 mm to 62.4 mm',
              'Nothing at all',
              'We rewrote it in Word Blocks',
              'We made it use the colour sensors'],
    why: 'Our wheels are smaller, so 30 cm needs more wheel turn.'
  },
  {
    title: 'What does our robot use to steer?',
    choices: ['Only the gyroscope',
              'The colour sensors following the lines',
              'The light sensor and the gyroscope together',
              'A timer'],
    why: 'The colour sensors are plugged in, but only the gyroscope steers.'
  },
  {
    title: 'What is yaw?',
    choices: ['The direction the robot is pointing, in degrees, like a compass',
              'How fast the robot is driving',
              'How far the robot has driven',
              'How much the robot is tipping forwards'],
    why: 'The gyroscope in the hub measures yaw.'
  },
  {
    title: 'When do we zero the yaw?',
    choices: ['At the start of every mission program',
              'Only once at the start of the season',
              'After every turn',
              'Never'],
    why: 'Zeroing makes the way the robot points at the start become 0.'
  },
  {
    title: 'What are our three gyroscope steps, in order?',
    choices: ['Zero the yaw, turn with the gyroscope, keep driving straight',
              'Turn, zero the yaw, stop',
              'Drive straight, then zero the yaw, then turn',
              'Read the colour sensor, turn, zero the yaw'],
    why: 'Zero at the start, turn with face, and correct while driving.'
  },
  {
    title: 'face(90) turns until the robot points 90 degrees from where?',
    choices: ['From the way it pointed when the yaw was zeroed at the start',
              'From wherever it points right now',
              'From the nearest wall',
              'From the left home'],
    why: 'Measuring from the start means small mistakes do not add up.'
  },
  {
    title: 'While driving straight, the robot drifts 5 degrees to the left. What ' +
           'does the code do?',
    choices: ['Steers back to the right, harder the further off it is',
              'Stops at once',
              'Keeps going and fixes it at the end',
              'Turns all the way round'],
    why: 'It checks the yaw every 15 milliseconds and steers back.'
  },
  {
    title: 'How often does drive_cm check the yaw?',
    choices: ['Every 15 milliseconds, about 66 times a second',
              'Once at the start',
              'Once a second',
              'Only at the end of the drive'],
    why: 'That is why small drifts never get big.'
  }
];

var OPEN = [
  ['Explain the robo taxi to a judge, in your own words.', ''],
  ['Time is our biggest limit. Give two things we did to save time.', ''],
  ['Explain yaw and our three gyroscope steps, the way you would say it to a ' +
   'judge.', ''],
  ['Why do we use push and pull attachments where we can?', ''],
  ['Which part of the five-minute explanation are you giving, and what is the ' +
   'one thing you most want the judges to remember?', ''],
  ['What do you still not understand, that we should sort out in class?',
   '"I don\'t know" is a good answer if it is true.']
];

// n is the question's place in the whole quiz. The right choice lands at a
// different position each time, so "always pick the first one" does not work.
function addQuizItem(form, q, n) {
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
        .setText('Not quite. Read ' + GUIDE + ' again.')
        .addLink(GUIDE_URL, 'Our key facts')
        .build());
  return item;
}

function createStrategyQuizForm() {
  var form = FormApp.create('FLL BIOGLOW: Strategy and design quiz');

  form.setDescription(
    'Read ' + GUIDE + ' first, and keep it open: ' + GUIDE_URL + ' . ' +
    'Looking things up is allowed. Parts 1 to 3 are marked as soon as you ' +
    'submit, and you can take the quiz again as many times as you like. ' +
    'Part 4 has no right answers.');

  form.setIsQuiz(true);
  // No email collection, so no login is needed, and no children's addresses
  // end up in the sheet. Same reasoning as the other forms.
  form.setCollectEmail(false);
  form.setAllowResponseEdits(true);
  form.setLimitOneResponsePerUser(false);
  form.setShowLinkToRespondAgain(true);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    'Done. Press "View score". If you missed one, read the hint, go back to ' +
    'the guide, and try again.');

  form.addListItem()
    .setTitle('Who is writing this?')
    .setChoiceValues(TEAM_NAMES.concat(['Coach']))
    .setRequired(true);

  var n = 0;
  form.addSectionHeaderItem()
    .setTitle('Part 1: How we chose our missions')
    .setHelpText('One point each.');
  MISSION_QUIZ.forEach(function (q) { addQuizItem(form, q, n++); });

  form.addSectionHeaderItem()
    .setTitle('Part 2: The robot and attachments')
    .setHelpText('One point each.');
  ROBOT_QUIZ.forEach(function (q) { addQuizItem(form, q, n++); });

  form.addSectionHeaderItem()
    .setTitle('Part 3: The code and the gyroscope')
    .setHelpText('One point each.');
  CODE_QUIZ.forEach(function (q) { addQuizItem(form, q, n++); });

  form.addPageBreakItem()
    .setTitle('Part 4: Say it your way')
    .setHelpText('No marks. Write it the way you would say it to a judge. ' +
                 'Short is fine.');
  OPEN.forEach(function (q) {
    var item = form.addParagraphTextItem().setTitle(q[0]);
    if (q[1]) item.setHelpText(q[1]);
  });

  Logger.log('--- For docs/team-links.md (kept off the public site) ---');
  Logger.log('Quiz for the kids: ' + form.getPublishedUrl());
  Logger.log('Edit the quiz: ' + form.getEditUrl());
  Logger.log('');
  Logger.log('Next: publish the form, set the quiz settings listed at the top');
  Logger.log('of this script, then Responses tab > Sheets icon.');
}
