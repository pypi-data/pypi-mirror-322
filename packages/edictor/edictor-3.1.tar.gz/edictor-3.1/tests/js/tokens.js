function tokens2alignment (tokens, alignment){
  var i;
  var new_alm = [];
  var sidx = 0;
  for (i=0; i<alignment.length; i++) {
    next_alm = alignment[i];
    if ("(-)".indexOf(next_alm) == -1) {
      new_alm.push(tokens[sidx]);
      sidx += 1;
    }
    else {
      new_alm.push(next_alm);
    }
  }
  if (sidx != tokens.length) {
    new_alm = tokens.join(" ");
  }
  else {
    new_alm = new_alm.join(" ");
  }
  return new_alm
};

console.log(tokens2alignment("mat", "(m-)at-"));
