# ROS2 Example Robot

Apenas um projeto simples de um robô em ROS. Tudo o que
você vê aqui foi feito a partir do que se aprendeu aqui:

ROS2: https://youtube.com/playlist?list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT&si=fMnu9wXx392EqEM-

OpenCV: https://youtube.com/playlist?list=PLzMcBGfZo4-lUA8uGjeXhBUUzPYc6vZRn&si=GGOUwLyZHhO_23Fo

MediaPipe: https://youtu.be/06TE_U21FK4?si=SDNOHs7BXYpP67f4

## Build

```cmd
colcon build --symlink-install
```

## Executando a simulação

Cada um dos trechos abaixo precisa ser executado em um terminal diferente.
Diretório de origem dos comandos: este aqui mesmo (example_robot).

1. iniciar o nó do robô:
```cmd
source install/setup.bash
ros2 launch robot_main robot.launch.py use_sim_time:=true
```

2. iniciar o gazebo pré-configurado para comunicar com ROS2:
```cmd
source install/setup.bash
ros2 launch gazebo_ros gazebo.launch.py
```

3. inserir o robô no Gazebo:
```cmd
source install/setup.bash
ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity some_robot_name
```

4. iniciar o nó que permite comandar manualmente o robô através do tópico cmd_vel 
```cmd
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Este último nó **precisa** estar em primeiro plano para
comandar o robô, portanto é recomendado executá-lo em um
terminal destacado do VS Code. Felizmente ele não exige estar
no mesmo diretório que o projeto pois é um nó de exemplo
padrão do ROS2.


## Câmera

Para inicializar o nó da câmera, mais um terminal:
```
source install/setup.bash
ros2 run robot_camera camera_node
```

E para visualizar a mensagem publicada, mais outro terminal:
```
ros2 run rqt_image_view rqt_image_view
```

escoha o tópico /camera e seja feliz.