## Usage

### running

```shell
cd src

# check help
python feat_generator.py -h

# generate 500 valid sample and dump to csv
python feat_generator.py -n 500 -d
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

- [ ] statistics
- [ ] visualization

### 2022/08/14

- [x] 【FINISHED】【working】通过基本 `FeildType` 限定数据定义域，然后进行 `item` 级别验证
- [x] 【DEPRECIATED】【todo, better-engineering but harder】通过基本 `FeildType` 限定数据定义域 + 统计信息，然后进行 `item` 级别验证