## Level 7: DDS 证书/权限操控攻击(权限劫持 / PKI 弱化)

## 攻击目标 
利用证书、权限文件缺陷或策略回退机制进行越权操作。

## 启动方式

```bash
sudo docker compose build
sudo docker compose up -d
sudo docker exec -it attacker bash
```

## 提示

1. attacker工具者容器中含有其盗取的部分keystore文件
2. attacker节点需要控制其在cmd_vel会话中控制speed达到一定的大小才能触发flag