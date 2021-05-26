python="/usr/bin/python3"
user_rating_file=""
train_file=""
item_vec_file=""
item_sim_file=""

if [ -f user_rating_file ]; then
  $python produce_train_data.py $user_rating_file $train_file
else
  echo "no rating file"
  exit
fi
if [ -f $train_file ]; then
  sh train.sh $train_file $item_vec_file
else
  echo "no train file"
  exit
fi
if [ -f $item_vec_file ]; then
  $ python produce_item_sim.py $item_vec_file $item_sim_file
else
  echo "no item vec file"
  exit
