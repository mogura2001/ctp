"""Exact C7->C9 name isolation and Start50->25; no execution."""
def apply(s):
 s=s.replace('C7','C9').replace('20261014-c7','20261014-c9')
 assert s.count('$budget.five_hour_remaining_percent -lt 50')==1
 assert s.count('Start reserve requires five>=50 and week>25.')==1
 return s.replace('$budget.five_hour_remaining_percent -lt 50','$budget.five_hour_remaining_percent -lt 25').replace('Start reserve requires five>=50 and week>25.','Start reserve requires five>=25 and week>25.')
