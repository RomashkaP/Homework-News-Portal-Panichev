#1.Создать двух пользователей.
User.objects.create_user('Chak Polanik')
User.objects.create_user('Tim Burton')

#2.Создать два объекта модели Author, связанные с пользователями.
user1 = User.objects.get(username='Chak Polanik')
user2 = User.objects.get(username='Tim Burton')
Author.objects.create(user=user1)
Author.objects.create(user=user2)

#3.Добавить 4 категории в модель Category.
Category.objects.create(name='Exclusive')
Category.objects.create(name='Finance')
Category.objects.create(name='Weather')
Category.objects.create(name='Politics')

#4.Добавить 2 статьи и 1 новость.
Post.objects.create(author=Author.objects.get(id=1), type='AR', title='Title of first article', text='Text of first article')
Post.objects.create(author=Author.objects.get(id=1), type='AR', title='Title of second article', text='Text of second article')
Post.objects.create(author=Author.objects.get(id=2), type='NW', title='Title of first news', text='Text of first news')

#5.Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post_id=1, category_id=1)
PostCategory.objects.create(post_id=1, category_id=3)
PostCategory.objects.create(post_id=1, category_id=3)
PostCategory.objects.create(post_id=2, category_id=3)
PostCategory.objects.create(post_id=2, category_id=4)
PostCategory.objects.create(post_id=3, category_id=4)

#6.Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(post_id=1, user_id=3, text='Text comment')
Comment.objects.create(post_id=2, user_id=4, text='Text comment')
Comment.objects.create(post_id=3, user_id=3, text='Text comment')
Comment.objects.create(post_id=1, user_id=4, text='Text comment')

#7.Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(id=3).like()
Post.objects.get(id=2).dislike()
Comment.objects.get(id=2).dislike()
Comment.objects.get(id=3).like()

#8.Обновить рейтинги пользователей.
Author.objects.get(id=1).updating_rating()
Author.objects.get(id=2).updating_rating()

#9.Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best = Author.objects.order_by('-rating')[0]
best.user.username

#10.Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
bestpost = Post.objects.order_by('-rating').first()
bestpost.values('author__user__username', 'time_in', 'rating', 'title').first()
bestpost.preview()

#11.Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=bestpost).values('time_in', 'user__username', 'rating', 'text')




