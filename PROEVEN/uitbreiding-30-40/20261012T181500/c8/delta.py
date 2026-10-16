"""Exact C7->C8 name isolation and Start50->40; no execution."""
def apply(s):
 s=s.replace('C7','C8').replace('20261014-c7','20261014-c8')
 assert s.count('$budget.five_hour_remaining_percent -lt 50')==1
 assert s.count('Start reserve requires five>=50 and week>25.')==1
 return s.replace('$budget.five_hour_remaining_percent -lt 50','$budget.five_hour_remaining_percent -lt 40').replace('Start reserve requires five>=50 and week>25.','Start reserve requires five>=40 and week>25.')
