
heroku pg:reset;
PGUSER=postgres PGPASSWORD=mylenana  heroku pg:push postgres://127.0.0.1:9011/manioc21 postgresql-acute-54160;