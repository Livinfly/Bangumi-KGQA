if __name__ == '__main__':

    print('谱酱: 少女祈祷中~')
    
    from question2answer import q2a

    print('谱酱: 现在可以问ACG相关的问题了喵~')
    while True:
        question = input('用户: ')
        if question == '谢谢你，谱酱！':
            print('谱酱:', '没事喵~')
            break
        print('谱酱:', q2a(question))