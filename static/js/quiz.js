// ============================================================
// IQ MASTER - Quiz Questions (60 total, 20 per category)
// ============================================================

const allQuestions = {

  mathematical: [
    { question: "What comes next in the series? 2, 4, 8, 16, ?", options: ["18", "24", "32", "30"], answer: 2 },
    { question: "If 5 × 4 = 20, what is 15 × 4?", options: ["45", "55", "60", "65"], answer: 2 },
    { question: "What is 25% of 200?", options: ["25", "40", "50", "75"], answer: 2 },
    { question: "Which number is missing? 1, 4, 9, 16, ?, 36", options: ["20", "25", "28", "30"], answer: 1 },
    { question: "What is the square root of 144?", options: ["10", "11", "12", "13"], answer: 2 },
    { question: "If a train travels 60 km/h for 2.5 hours, how far does it travel?", options: ["120 km", "140 km", "150 km", "160 km"], answer: 2 },
    { question: "What is 15% of 300?", options: ["30", "40", "45", "50"], answer: 2 },
    { question: "Complete the series: 3, 6, 12, 24, ?", options: ["36", "42", "48", "54"], answer: 2 },
    { question: "If 3x = 21, what is x?", options: ["5", "6", "7", "8"], answer: 2 },
    { question: "What is 2³ + 3²?", options: ["13", "15", "17", "19"], answer: 2 },
    { question: "A rectangle has length 8 and width 5. What is its area?", options: ["30", "35", "40", "45"], answer: 2 },
    { question: "What comes next? 100, 95, 85, 70, ?", options: ["50", "55", "60", "65"], answer: 0 },
    { question: "If 20% of a number is 50, what is the number?", options: ["200", "225", "250", "275"], answer: 2 },
    { question: "What is the next prime number after 13?", options: ["14", "15", "16", "17"], answer: 3 },
    { question: "Simplify: (4 + 6) × 3 - 5", options: ["20", "25", "28", "30"], answer: 1 },
    { question: "What is 1/4 + 1/2?", options: ["1/6", "2/6", "3/4", "1"], answer: 2 },
    { question: "A shop sells items at 20% discount. Original price is ₹500. Sale price?", options: ["₹350", "₹380", "₹400", "₹420"], answer: 2 },
    { question: "What is the LCM of 4 and 6?", options: ["8", "10", "12", "24"], answer: 2 },
    { question: "Complete: 2, 3, 5, 8, 13, ?", options: ["18", "19", "20", "21"], answer: 3 },
    { question: "If a = 3 and b = 4, what is a² + b²?", options: ["20", "25", "30", "35"], answer: 1 },
  ],

  logical: [
    { question: "Which number is the odd one out? 3, 5, 7, 10, 11", options: ["3", "5", "10", "11"], answer: 2 },
    { question: "If CAT = 24, then DOG = ?", options: ["26", "30", "32", "34"], answer: 0 },
    { question: "All roses are flowers. Some flowers fade quickly. Therefore:", options: ["All roses fade quickly", "Some roses may fade quickly", "No roses fade quickly", "Roses never fade"], answer: 1 },
    { question: "Find the odd one out: Apple, Mango, Carrot, Banana", options: ["Apple", "Mango", "Carrot", "Banana"], answer: 2 },
    { question: "If FIRE = 6935, what does RICE = ?", options: ["9357", "3956", "9365", "3965"], answer: 0 },
    { question: "A is taller than B. B is taller than C. Who is shortest?", options: ["A", "B", "C", "Cannot determine"], answer: 2 },
    { question: "Monday is 2 days after Saturday. What day is 3 days before Wednesday?", options: ["Monday", "Sunday", "Saturday", "Friday"], answer: 1 },
    { question: "Which word does NOT belong? Swift, Fast, Quick, Slow, Rapid", options: ["Swift", "Fast", "Slow", "Rapid"], answer: 2 },
    { question: "If all Blops are Razzles, and all Razzles are Lazzles, are all Blops Lazzles?", options: ["Yes", "No", "Maybe", "Cannot determine"], answer: 0 },
    { question: "Find the pattern: AZ, BY, CX, ?", options: ["DE", "DW", "EW", "EV"], answer: 1 },
    { question: "5 people are in a room. Each shakes hands with every other once. Total handshakes?", options: ["8", "10", "12", "15"], answer: 1 },
    { question: "If you rearrange CIFAIPC, you get a:", options: ["Country", "Ocean", "City", "Animal"], answer: 1 },
    { question: "Which is different? 144, 169, 196, 216, 225", options: ["144", "169", "216", "225"], answer: 2 },
    { question: "A clock shows 3:15. What angle do the hands form?", options: ["0°", "7.5°", "15°", "22.5°"], answer: 1 },
    { question: "Tom is Sam's brother. Sam is Kate's son. How is Tom related to Kate?", options: ["Father", "Uncle", "Son", "Brother"], answer: 2 },
    { question: "Find the missing: 2, 6, 12, 20, 30, ?", options: ["40", "42", "44", "46"], answer: 1 },
    { question: "If RED is coded as 27, then BLUE = ?", options: ["40", "43", "46", "49"], answer: 1 },
    { question: "Which shape has the most sides? Pentagon, Hexagon, Octagon, Heptagon", options: ["Pentagon", "Hexagon", "Heptagon", "Octagon"], answer: 3 },
    { question: "A man walks 5km North, then 3km East. How far is he from start (approx)?", options: ["5.8 km", "6.2 km", "7.0 km", "8.0 km"], answer: 0 },
    { question: "If PAPER is to WRITE, then KNIFE is to ?", options: ["Eat", "Cut", "Cook", "Sharpen"], answer: 1 },
  ],

  puzzle: [
    { question: "I have cities but no houses. I have mountains but no trees. I have water but no fish. What am I?", options: ["A dream", "A map", "A painting", "A mirror"], answer: 1 },
    { question: "The more you take, the more you leave behind. What am I?", options: ["Time", "Money", "Footsteps", "Memories"], answer: 2 },
    { question: "What has hands but can't clap?", options: ["A tree", "A clock", "A glove", "A statue"], answer: 1 },
    { question: "I speak without a mouth and hear without ears. I have no body but come alive with wind. What am I?", options: ["A ghost", "An echo", "A shadow", "A dream"], answer: 1 },
    { question: "Which piece completes the pattern? 🟥🟦🟥 / 🟦🟥🟦 / 🟥🟦?", options: ["🟥", "🟦", "🟩", "🟨"], answer: 0 },
    { question: "A rooster lays an egg on top of a barn roof. Which way does it roll?", options: ["Left", "Right", "North", "Roosters don't lay eggs"], answer: 3 },
    { question: "If you have me, you want to share me. If you share me, you no longer have me. What am I?", options: ["Money", "Food", "A secret", "Time"], answer: 2 },
    { question: "What can travel around the world while staying in a corner?", options: ["The sun", "A stamp", "Wind", "A shadow"], answer: 1 },
    { question: "Two fathers and two sons go fishing. They each catch one fish. Only 3 fish total. How?", options: ["One escaped", "They shared", "Grandfather, father, son", "One didn't catch"], answer: 2 },
    { question: "What gets wetter the more it dries?", options: ["Rain", "A towel", "A sponge", "Ice"], answer: 1 },
    { question: "Forward I am heavy, backward I am not. What am I?", options: ["Time", "Ton", "Stone", "Load"], answer: 1 },
    { question: "Complete the pattern: 1, 11, 21, 1211, 111221, ?", options: ["312211", "123121", "211231", "321121"], answer: 0 },
    { question: "Which image completes the sequence? △ ▲ △▲ ▲△ ?", options: ["△△", "▲▲", "△▲△", "▲△▲"], answer: 2 },
    { question: "A box has no hinges, no lock, no key, yet a golden treasure lies inside. What is it?", options: ["A chest", "An egg", "A safe", "A walnut"], answer: 1 },
    { question: "I have a head and a tail but no body. What am I?", options: ["A snake", "A coin", "A needle", "A pin"], answer: 1 },
    { question: "What comes once in a minute, twice in a moment, never in a thousand years?", options: ["A second", "The letter M", "A blink", "A heartbeat"], answer: 1 },
    { question: "Find the next: 🔴🔵🟢🔴🔵?", options: ["🔴", "🔵", "🟢", "🟡"], answer: 2 },
    { question: "If you throw a red stone into the blue sea, what does it become?", options: ["Blue", "Purple", "Wet", "It sinks"], answer: 2 },
    { question: "What word becomes shorter when you add two letters to it?", options: ["Long", "Short", "Brief", "Small"], answer: 1 },
    { question: "I am always in front of you but cannot be seen. What am I?", options: ["The future", "Air", "Your nose", "A mirror"], answer: 0 },
  ]

};

// ============================================================
// Get category from URL parameter
// ============================================================
function getCategory() {
  const params = new URLSearchParams(window.location.search);
  return params.get('category') || 'logical';
}

const selectedCategory = getCategory();
const questions = allQuestions[selectedCategory] || allQuestions['logical'];