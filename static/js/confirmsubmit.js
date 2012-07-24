function confirmsubmit(path) {
  if (confirm("You sure you want to delete?")) {
    document.location = path;
  }
    
  return false;
}