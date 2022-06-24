USE dojo_kata;

INSERT INTO Training (trainingId,title,sensei,details)
VALUES
    (1,"Linux administration basics", "shihan", "Learn how to use basics Linux commands to get familiar with the command-line.");

INSERT INTO Workshop(workshopId,title,details,trainingId)
VALUES
    (1,"Basics: list files","Learn useful commands that show files using command-line.",1),
    (2,"Basics: files permissions","Learn useful commands that administrate permissions of files (ie. groups, owner...).",1);

INSERT INTO Imagebox(rootLogin,userLogin,userPassword,filename,type,os,accessProtocol,options,workshopId)
VALUES
    ("root","ubuntu","ubuntu","demo_ubuntu_server.ova","VirtualBox","Ubuntu","http",NULL,1),
    ("root","ubuntu","ubuntu","demo_ubuntu_server.ova","VirtualBox","Ubuntu","http",NULL,2);
