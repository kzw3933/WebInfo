
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND DIVIDE LPAREN MINUS NAME NOT NUMBER OR PLUS RPAREN TIMESEXPR : ORLIST\n     ORLIST : ORLIST OR ANDLIST\n        | ANDLIST\n    \n     ANDLIST : ANDLIST AND LIST\n        | LIST\n    \n     LIST : LPAREN ORLIST RPAREN\n        | NOT LPAREN ORLIST RPAREN\n        | NAME\n        | NOT NAME\n    '
    
_lr_action_items = {'LPAREN':([0,5,6,8,9,11,],[5,5,11,5,5,5,]),'NOT':([0,5,8,9,11,],[6,6,6,6,6,]),'NAME':([0,5,6,8,9,11,],[7,7,12,7,7,7,]),'$end':([1,2,3,4,7,12,13,14,15,17,],[0,-1,-3,-5,-8,-9,-2,-4,-6,-7,]),'OR':([2,3,4,7,10,12,13,14,15,16,17,],[8,-3,-5,-8,8,-9,-2,-4,-6,8,-7,]),'RPAREN':([3,4,7,10,12,13,14,15,16,17,],[-3,-5,-8,15,-9,-2,-4,-6,17,-7,]),'AND':([3,4,7,12,13,14,15,17,],[9,-5,-8,-9,9,-4,-6,-7,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'EXPR':([0,],[1,]),'ORLIST':([0,5,11,],[2,10,16,]),'ANDLIST':([0,5,8,11,],[3,3,13,3,]),'LIST':([0,5,8,9,11,],[4,4,4,14,4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> EXPR","S'",1,None,None,None),
  ('EXPR -> ORLIST','EXPR',1,'p_expr','syntax_book.py',88),
  ('ORLIST -> ORLIST OR ANDLIST','ORLIST',3,'p_orList','syntax_book.py',94),
  ('ORLIST -> ANDLIST','ORLIST',1,'p_orList','syntax_book.py',95),
  ('ANDLIST -> ANDLIST AND LIST','ANDLIST',3,'p_andList','syntax_book.py',106),
  ('ANDLIST -> LIST','ANDLIST',1,'p_andList','syntax_book.py',107),
  ('LIST -> LPAREN ORLIST RPAREN','LIST',3,'p_list','syntax_book.py',118),
  ('LIST -> NOT LPAREN ORLIST RPAREN','LIST',4,'p_list','syntax_book.py',119),
  ('LIST -> NAME','LIST',1,'p_list','syntax_book.py',120),
  ('LIST -> NOT NAME','LIST',2,'p_list','syntax_book.py',121),
]
