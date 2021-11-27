nnoremap <silent> <buffer> <localleader>c :execute "ShowCreateTable"<cr>
xnoremap <silent> <expr> <localleader>v  mysql#send_message("") 
nnoremap <silent> <buffer> <c-l>  :call mysql#send_message_c_l()<cr> 
nnoremap <silent> <buffer> <localleader>q  :call mysql#send_message_q()<cr> 

if exists("b:current_syntax")
  finish
endif

" Convert deprecated variable to new one
if exists('g:vue_disable_pre_processors') && g:vue_disable_pre_processors
  let g:vue_pre_processors = []
endif

runtime! syntax/mysql.vim
unlet b:current_syntax

let b:current_syntax = "my"
