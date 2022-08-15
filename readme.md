## Usage

### running

```shell
cd src

# check help
python main.py -h

# generate 500 valid sample and dump to csv
python main.py -n 500 -d
```

### running result

```text
(venv) 2022/08/15 04:02:16 (base) ➜  src git:(master) ✗ python feat_generator.py -n 500
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 500/500 [02:24<00:00,  3.45it/s]
2022-08-15 04:17:25,630, INFO     [feat_generator.py:feat_generator:genFeatModels:191] {'config': {'target models': 500, 'max retries': 10}, 'tries': {'failed': 60, 'total': 560}}
2022-08-15 04:17:25,649, INFO     [feat_generator.py:feat_generator:dump:207] dumped to file:///Users/mark/PycharmProjects/lxw-game-data/output/feat_models.csv
```

## Track

### 2022/08/15

table relative:
- [ ] 1.输出的格式应该和原数据集保持一致，就是性别年龄什么的都带上。特别是五个人格得分应该每一行都有。
- [ ] 2.目前是500个数据，但是重点是10个为一组，这一组的是同一个人的，因此性别年龄五个人格得分应该相同，并且这个分组在数据集要有体现（比如同一个userID）。
- [ ] 10.属性列的顺序能不能和原有数据集保持一致，这样我好复用一些代码

feature distribution:
以下两点，应该已解决，通过调整xdata [0, .25, 0.5, .75, .97] --> [0, .1, .5, .9, .97]
- [x] 【从分布上看，0.几的小数比较多是难免的，因为拟合结果很指数，所以目前采用了0-->0.8的边界设定】4.storyTime小于1的太多了 好多是0.00xxx的 500个里面小于1的最好不要超过10个
- [x] 8.batteryTimes大于8次的太多了，能不能把比例控制在10%以内
- [x] 9.signalTimes，filterLenTimes的值域是0-5.(这个是我的失误，我当时搞错了)

output formats:
- [x] 3.clickRate是整型，不带小数
- [x] 【声明数据类型时用int，不用bool就可以以TRUE/FALSE赋值，但以1/0表示与输出了】11.布尔类型的，能不能有一份0,1的表达，就是0代表false，1代表true。（两种格式可以都输出，数字比较好跑东西，文字人看容易一些）
- [ ] 7.百分比相关的保留4位小数就可以了。
- [ ] storyTime 保留1位小数就行了。
- [ ] 5.tutorialTime保留1位小数就行了。
- [ ] 6.score保留1位小数就行了。


- [ ] statistics
- [ ] visualization

### 2022/08/14

- [x] 【FINISHED】【working】通过基本 `FeildType` 限定数据定义域，然后进行 `item` 级别验证
- [x] 【DEPRECIATED】【todo, better-engineering but harder】通过基本 `FeildType` 限定数据定义域 + 统计信息，然后进行 `item` 级别验证