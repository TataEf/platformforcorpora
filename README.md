#platformforcorpora
<p>в этом репозитории находятся неоходимые файлы для создания корпуса электронной почты.</p>

####foruser.py
программе на вход подаются файлы cutlocations.txt, cutnamesforbegin.txt, cutnamesformiddle.txt, cutsurnames.txt, info.txt и .txt-файл, сожержащий в названии emails и нормер c кодировкой UTF-8. Например: emails5.txt. Письма в файле должны быть разделены тегом \<END\>.

####encrypt.ipynb
на вход - файл deletedwords.txt (создается в foruser.py)
создает yourdecryptionkey.txt, youencryptionkey.txt, researchernkey.txt
для работы программы нужны дополнительные модули (pycrypto)

####decrypt.ipynb
на вход - файлы deletedwords.txt, yourdecryptionkey.txt, researcherkey.txt
для работы программы нужны дополнительные модули (pycrypto)


####forresearcher.py
программе подаются на вход папки с названиями user1, user2 и т.д. в каждой из папок должны быть файлы с кодировкой UTF-8 и форматом txt changedemails, deletedwords, sessionkey, socialinfo (автоматически создаются описанными выше программами(foruser.py,encrypt.ipynb)

####infobase_decryption.ipynb
на вход - infobase.json (создается в forresearcher.py)
создает decryptionkey.txt, encryptionkey.txt, sessionkey.txt
для работы программы нужны дополнительные модули (pycrypto)

####infobase_incryption.ipynb
на вход - decryptionkey.txt, sessionkey.txt (создается в infobase_decryption.ipynb)
для работы программы нужны дополнительные модули (pycrypto)
