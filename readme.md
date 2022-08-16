## Usage

### running

```shell
cd src

# check help
python main.py -h

usage: main.py [-h] [--no-regen-users] [--no-dump] [--users-cnt USERS_CNT] [--user-times USER_TIMES] [--perturbation PERTURBATION] [--main-space MAIN_SPACE] [--nMaxGenRetries NMAXGENRETRIES]

optional arguments:
  -h, --help            show this help message and exit
  --no-regen-users      regenerate users data from xlsx to json
  --no-dump             dump the feature models to file
  --users-cnt USERS_CNT
                        users to generate
  --user-times USER_TIMES
                        run times of each user
  --perturbation PERTURBATION
                        perturbation based on the target value, range: (0, 1), 0: always target; 1: always random
  --main-space MAIN_SPACE
                        decides the main space based on center on domain; range: (0,1); 0: normal, 1: always center
  --nMaxGenRetries NMAXGENRETRIES
                        number of retrying to generate models in each epoch, recommending 5-10

```

### running result

```text
/Users/mark/coding/PycharmProjects/lxw-game-data/venv/bin/python /Users/mark/coding/PycharmProjects/lxw-game-data/src/main.py
2022-08-16 17:48:35,036 INFO     [main.py:77] <MAIN> Namespace(no_regen_users=False, no_dump=False, users_cnt=50, user_times=10, perturbation=0.3, main_space=0.8, nMaxGenRetries=10)
2022-08-16 17:48:35,365 INFO     [regeneate_users.py:21] <utils-regen-users> read data from file:///Users/mark/coding/PycharmProjects/lxw-game-data/data/精简版数据集.xlsx
2022-08-16 17:48:35,419 INFO     [regeneate_users.py:27] <utils-regen-users> regenerated users to file:///Users/mark/coding/PycharmProjects/lxw-game-data/output/users.json
100%|██████████| 50/50 [00:00<00:00, 60.42it/s]
2022-08-16 17:48:36,269 INFO     [main.py:97] <MAIN> done generating all the 50 users with 500 models
2022-08-16 17:48:36,297 INFO     [dump.py:38] <utils-dump> dumped to file:///Users/mark/coding/PycharmProjects/lxw-game-data/output/models.csv

Process finished with exit code 0
```

## Track

### 2022/08/16

主要是原数据表数据有较大问题，导致生成经常有bug。

减弱一些限制条件、修改一些原数据后已能顺利输出程序。

### 2022/08/15

- [ ] statistics
- [ ] visualization

#### validation

data relative:
- [x] 1.输出的格式应该和原数据集保持一致，就是性别年龄什么的都带上。特别是五个人格得分应该每一行都有。
- [x] 2.目前是500个数据，但是重点是10个为一组，这一组的是同一个人的，因此性别年龄五个人格得分应该相同，并且这个分组在数据集要有体现（比如同一个userID）。

table relative:
- [x] 10.属性列的顺序能不能和原有数据集保持一致，这样我好复用一些代码

feature distribution:
> 以下两点，应该已解决，通过调整xdata [0, .25, 0.5, .75, .97] --> [0, .1, .5, .9, .97]
- [x] 4.storyTime小于1的太多了 好多是0.00xxx的 500个里面小于1的最好不要超过10个
- [x] 8.batteryTimes大于8次的太多了，能不能把比例控制在10%以内
- [x] 9.signalTimes，filterLenTimes的值域是0-5.(这个是我的失误，我当时搞错了)
> 通过使用更低级的api `_gen_float` 应该完成了：
- [x] mismatchRate 应该保证80%的数据结果都在20%以下
- [x] badRate值域改成0-70%吧
- [x] getbackRate 应该保证80%的数据结果都在50%以下
- [x] hitRate应该保证80%的数据结果都在50%以上

output formats:
- [x] 3.clickRate是整型，不带小数
> 声明数据类型时用int，不用bool就可以以TRUE/FALSE赋值，但以1/0表示与输出了:
- [x] 11.布尔类型的，能不能有一份0,1的表达，就是0代表false，1代表true。（两种格式可以都输出，数字比较好跑东西，文字人看容易一些）
- [x] 7.百分比相关的保留4位小数就可以了。
- [x] storyTime 保留1位小数就行了。
- [x] 5.tutorialTime保留1位小数就行了。
- [x] 6.score保留1位小数就行了。

### 2022/08/14

- [x] 【FINISHED】【working】通过基本 `FeildType` 限定数据定义域，然后进行 `item` 级别验证
- [x] 【DEPRECIATED】【todo, better-engineering but harder】通过基本 `FeildType` 限定数据定义域 + 统计信息，然后进行 `item` 级别验证