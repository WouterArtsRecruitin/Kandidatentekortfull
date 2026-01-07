// Test file with intentional code quality issues for Claude to review

function calculateTotal(items: any[]) {
  var total = 0;
  for (var i = 0; i < items.length; i++) {
    total = total + items[i].price;
  }
  return total;
}

// Missing error handling
function fetchUserData(userId: string) {
  const response = fetch(`/api/users/${userId}`);
  return response.json();
}

// Unused variable
const unusedVar = "This should be flagged";

export { calculateTotal, fetchUserData };
