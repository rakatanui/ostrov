from datetime import datetime, timezone
from textwrap import dedent

from django.db import migrations


SERIES_SEED = {
    "translations": [
        {
            "locale": "ru",
            "name": "Сфера Шафтара",
            "slug": "sfera-shaftara",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "en",
            "name": "the Sphere of Shaftar",
            "slug": "the-sphere-of-shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "de",
            "name": "the Sphere of Shaftar",
            "slug": "the-sphere-of-shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "es",
            "name": "la Esfera de Shaftar",
            "slug": "la-esfera-de-shaftar",
            "description": "",
            "is_published": True,
        },
    ]
}

PROVINCE_SEED = {
    "translations": [
        {
            "locale": "ru",
            "name": "Шафтар",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "en",
            "name": "Shaftar",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "de",
            "name": "Shaftar",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "es",
            "name": "Shaftar",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
    ]
}

PATRON_SEED = {
    "translations": [
        {
            "locale": "ru",
            "name": "Шафтар",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "en",
            "name": "Shaftar",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "de",
            "name": "Shaftar",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
        {
            "locale": "es",
            "name": "Shaftar",
            "slug": "shaftar",
            "description": "",
            "is_published": True,
        },
    ]
}

TAG_SEEDS = [
    {
        "translations": [
            {
                "locale": "ru",
                "name": "Красная Зима",
                "slug": "krasnaya-zima",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "en",
                "name": "the Crimson Winter",
                "slug": "the-crimson-winter",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "de",
                "name": "der Purpurwinter",
                "slug": "der-purpurwinter",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "es",
                "name": "el Invierno Carmesí",
                "slug": "el-invierno-carmesi",
                "description": "",
                "is_published": True,
            },
        ]
    },
    {
        "translations": [
            {
                "locale": "ru",
                "name": "берег деревянных скелетов",
                "slug": "bereg-derevyannyh-skeletov",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "en",
                "name": "the Shore of Wooden Skeletons",
                "slug": "the-shore-of-wooden-skeletons",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "de",
                "name": "die Küste der hölzernen Skelette",
                "slug": "die-kuste-der-holzernen-skelette",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "es",
                "name": "la Costa de los Esqueletos de Madera",
                "slug": "la-costa-de-los-esqueletos-de-madera",
                "description": "",
                "is_published": True,
            },
        ]
    },
    {
        "translations": [
            {
                "locale": "ru",
                "name": "рыжие",
                "slug": "ryzhie",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "en",
                "name": "red-haired",
                "slug": "red-haired",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "de",
                "name": "die Rothaarigen",
                "slug": "die-rothaarigen",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "es",
                "name": "los pelirrojos",
                "slug": "los-pelirrojos",
                "description": "",
                "is_published": True,
            },
        ]
    },
    {
        "translations": [
            {
                "locale": "ru",
                "name": "Хьёльм",
                "slug": "hyolm",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "en",
                "name": "Hjoelm",
                "slug": "hjoelm",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "de",
                "name": "Hjoelm",
                "slug": "hjoelm",
                "description": "",
                "is_published": True,
            },
            {
                "locale": "es",
                "name": "Hjoelm",
                "slug": "hjoelm",
                "description": "",
                "is_published": True,
            },
        ]
    },
]

LEGEND_SEED = {
    "status": "published",
    "published_at": datetime(2026, 3, 29, 19, 42, 9, tzinfo=timezone.utc),
    "hero_image": "",
    "translations": [
        {
            "locale": "ru",
            "title": "Рыжая осень",
            "slug": "ryzhaya-osen",
            "excerpt": (
                "Из «Сферы Шафтара». Рассказывать её дозволено только, когда "
                "северный ветер воет особенно злобно. Если расскажешь не в срок "
                "— ветер может забрать твой голос навсегда."
            ),
            "body": dedent(
                """
                Когда Владыка моря ещё только учил людей бояться своего гнева, а покровитель Шафтар уже правил северными горами и рудниками, с моря пришла беда, которую даже боги не ждали.

                Они явились ночью.

                Пять чёрных кораблей с парусами цвета свежей крови.
                На борту — воины, чьи волосы горели рыжим, как расплавленная медь в кузне покровителя. Кожа у них была белее снега на вершинах, а глаза — чёрные, без зрачков, будто две дыры в бездну. Они не кричали. Они не трубили в рога. Они просто шли на скалы, словно знали, что скалы их не удержат.

                Люди на берегу (а тогда там стояли первые рыбацкие деревни Шафтара) увидели их и поняли: это не захватчики. Это кара.

                Рыжие не грабили. Они не брали рабов. Они переписывали всё живое. Где ступала их нога — земля становилась красной, будто пропитанной кровью. Деревья начинали истекать красным соком, а люди, которых они касались, за несколько мгновений превращались в деревянные статуи — кожа трескалась, кости становились корой, глаза — смоляными каплями. Живые ещё кричали внутри этих статуй, но уже не могли пошевелиться.
                Они называли себя «Детьми Красной Зимы». Говорили, что пришли забрать Остров обратно — в вечную ночь и вечный холод, где нет ни Владык, ни Покровителей. Их вожак — огромный рыжебородый гигант по имени Хьёльм — носил на поясе ожерелье из человеческих языков и утверждал, что каждый язык когда-то молил о пощаде… а он всё равно забрал его.

                Шафтар, покровитель северного ветра, разозлился по-настоящему.

                Он обрушил на них свой полный гнев — ураган такой силы, что горы Шафтара до сих пор носят шрамы. Корабли разнесло в щепки. Воинов швыряло на острые скалы, как сухие листья. Море в тот день стало красным на много дней вперёд. Именно тогда берег получил имя берег деревянных скелетов — потому что тела рыжих, разбившиеся о камни, за ночь окаменели и стали похожи на кривые, скрученные деревья. А само событие жрецы назвали Рыжей осенью.

                Но пятеро всё-таки выжили.
                Они не просто уцелели. Они выбрались.
                Пятеро самых страшных — те, кто даже в агонии продолжал скалиться чёрными беззубыми ртами. Они ушли в самые глубокие расщелины северных гор Шафтара, туда, где даже рудники не копали. Там они основали крошечное поселение Валха — место, где до сих пор северный ветер поёт не песню Шафтара, а их собственную колыбельную.

                Говорят, в Валхе до сих пор живут их потомки.
                Они не стареют так, как люди. Их волосы остаются рыжими даже в могиле. А если в полнолуние кто-то забредёт слишком близко к северной оконечности… то услышит, как из-под земли доносится тихий, почти ласковый шёпот:

                «Мы вернёмся.
                Не все сразу.
                Но вернёмся».

                Именно поэтому в провинции Шафтар до сих пор существует закон: любой человек с рыжими волосами, должен либо обрить голову наголо, либо уйти на рудники добровольно. Потому что жрецы помнят: рыжие не погибли.
                Они просто ждут, когда северный ветер снова ослабеет.
                """
            ).strip(),
            "seo_title": "",
            "seo_description": "",
            "is_published": True,
        },
        {
            "locale": "en",
            "title": "The Red Autumn",
            "slug": "the-red-autumn",
            "excerpt": (
                "From “The Sphere of Shaftar.” This tale may be told only when "
                "the northern wind howls with particular malice. If you tell it "
                "out of season, the wind may steal your voice forever."
            ),
            "body": dedent(
                """
                In those days, when the Lord of the Sea was only beginning to teach men to fear his wrath, and the patron Shaftar already ruled the northern mountains and mines, a calamity came from the sea that even the gods had not expected.

                They came by night.

                Five black ships with sails the color of fresh blood.

                On board were warriors whose hair burned red like molten copper in the patron’s forge. Their skin was whiter than the snow on the peaks, and their eyes were black, without pupils, like two holes opening into the abyss. They did not shout. They did not sound their horns. They simply walked onto the rocks, as though they knew the rocks could not hold them.

                The people on the shore, where the first fishing villages of Shaftar then stood, saw them and understood: these were not invaders. This was punishment.

                The red-haired ones did not plunder. They did not take slaves. They rewrote all living things. Wherever their feet fell, the ground turned red, as though soaked in blood. Trees began to bleed crimson sap, and the people they touched were turned within moments into wooden statues: skin split apart, bones became bark, eyes hardened into drops of resin. The living still screamed inside those statues, but could no longer move.

                They called themselves the Children of the Crimson Winter. They said they had come to take the Island back into eternal night and eternal cold, where there would be neither Lords nor Patrons.

                Their leader, a gigantic red-bearded giant named Hjoelm, wore around his belt a necklace of human tongues and claimed that every tongue had once begged him for mercy... and he had taken it anyway.

                Shaftar, patron of the northern wind, grew truly enraged.

                He unleashed upon them the full force of his wrath, a storm so terrible that the mountains of Shaftar still bear its scars. The ships were smashed into splinters. The warriors were hurled against the jagged cliffs like dry leaves. For many days afterward the sea remained red. That was when the coast received its name, the Shore of Wooden Skeletons, because the bodies of the red-haired dead, shattered upon the rocks, turned to stone overnight and came to resemble twisted, crooked trees. And the priests gave the event its name: the Red Autumn.

                But five of them survived.

                They did not merely remain alive. They escaped.

                Five of the most terrible, the ones who, even in agony, still bared their black toothless mouths in a grin. They went into the deepest clefts of Shaftar’s northern mountains, into places where even the mines had never reached. There they founded a tiny settlement called Valkha, a place where, to this day, the northern wind sings not the song of Shaftar, but their own lullaby.

                It is said that their descendants still live in Valkha.

                They do not age as men do. Their hair remains red even in the grave. And if, under a full moon, someone strays too close to the northern tip of the land, he will hear a quiet, almost gentle whisper rising from beneath the earth:

                “We will return.
                Not all at once.
                But we will return.”

                That is why, in the province of Shaftar, a law still endures: any person with red hair must either shave his head bare or go willingly into the mines. For the priests remember: the red-haired ones did not perish.

                They are only waiting for the northern wind to weaken once again.
                """
            ).strip(),
            "seo_title": "",
            "seo_description": "",
            "is_published": True,
        },
        {
            "locale": "de",
            "title": "Der Rote Herbst",
            "slug": "der-rote-herbst",
            "excerpt": (
                "Aus der „Sphäre Shaftars“. Diese Legende darf nur dann erzählt "
                "werden, wenn der Nordwind besonders bösartig heult. Erzählt man "
                "sie zur falschen Zeit, kann der Wind einem für immer die Stimme "
                "rauben."
            ),
            "body": dedent(
                """
                Damals, als der Herr des Meeres die Menschen erst zu lehren begann, seinen Zorn zu fürchten, und der Schutzpatron Shaftar bereits über die nördlichen Berge und Bergwerke herrschte, kam vom Meer ein Unheil, das selbst die Götter nicht erwartet hatten.

                Sie kamen in der Nacht.

                Fünf schwarze Schiffe mit Segeln in der Farbe frischen Blutes.

                An Bord standen Krieger, deren Haar rot glühte wie geschmolzenes Kupfer in der Schmiede des Schutzpatrons. Ihre Haut war weißer als der Schnee auf den Gipfeln, und ihre Augen waren schwarz, ohne Pupillen, wie zwei Löcher in den Abgrund. Sie schrien nicht. Sie stießen nicht in Hörner. Sie gingen einfach auf die Felsen zu, als wüssten sie, dass die Felsen sie nicht aufhalten würden.

                Die Menschen an der Küste, wo damals die ersten Fischerdörfer Shaftars standen, sahen sie und begriffen: Das waren keine Eroberer. Das war Strafe.

                Die Rothaarigen plünderten nicht. Sie nahmen keine Sklaven. Sie schrieben alles Lebendige um. Wo ihr Fuß den Boden berührte, färbte sich die Erde rot, als wäre sie mit Blut getränkt. Die Bäume begannen, purpurroten Saft zu vergießen, und die Menschen, die sie berührten, verwandelten sich binnen Augenblicken in hölzerne Statuen: Die Haut platzte auf, die Knochen wurden zu Rinde, die Augen zu Harztropfen. Die Lebenden schrien noch immer in diesen Statuen, konnten sich aber nicht mehr bewegen.

                Sie nannten sich die Kinder des Purpurwinters. Sie sagten, sie seien gekommen, um die Insel zurückzuholen, in die ewige Nacht und die ewige Kälte, wo es weder Herrscher noch Schutzpatrone gebe.

                Ihr Anführer, ein riesenhafter rothaariger Hüne namens Hjoelm, trug an seinem Gürtel eine Kette aus menschlichen Zungen und behauptete, jede einzelne habe ihn einst um Gnade angefleht... und er habe sie trotzdem genommen.

                Shaftar, der Schutzpatron des Nordwinds, geriet in echten Zorn.

                Er ließ seinen ganzen Grimm auf sie niederfahren, einen Sturm von solcher Gewalt, dass die Berge Shaftars seine Narben bis heute tragen. Die Schiffe wurden in Splitter gerissen. Die Krieger wurden wie trockenes Laub gegen die scharfen Klippen geschleudert. Das Meer blieb viele Tage lang rot. Damals erhielt die Küste ihren Namen, die Küste der hölzernen Skelette, denn die Körper der Rothaarigen, die an den Felsen zerschmettert worden waren, versteinerten über Nacht und sahen aus wie krumme, verdrehte Bäume. Und die Priester gaben dem Ereignis seinen Namen: der Rote Herbst.

                Doch fünf von ihnen überlebten.

                Sie kamen nicht nur mit dem Leben davon. Sie entkamen.

                Fünf der Schrecklichsten, jene, die selbst in ihrer Qual noch mit schwarzen, zahnlosen Mündern grinsten. Sie zogen in die tiefsten Spalten der nördlichen Berge Shaftars, dorthin, wo nicht einmal die Bergwerke je gegraben hatten. Dort gründeten sie eine winzige Siedlung namens Valkha, einen Ort, an dem der Nordwind bis heute nicht das Lied Shaftars singt, sondern ihr eigenes Wiegenlied.

                Man sagt, ihre Nachkommen lebten noch immer in Valkha.

                Sie altern nicht wie Menschen. Ihr Haar bleibt selbst im Grab rot. Und wenn jemand bei Vollmond der nördlichsten Spitze des Landes zu nahe kommt, wird er aus der Erde ein leises, fast zärtliches Flüstern hören:

                „Wir werden zurückkehren.
                Nicht alle auf einmal.
                Aber wir werden zurückkehren.“

                Darum gibt es in der Provinz Shaftar bis heute ein Gesetz: Jeder Mensch mit rotem Haar muss sich entweder den Kopf kahl scheren oder freiwillig in die Bergwerke gehen. Denn die Priester erinnern sich: Die Rothaarigen sind nicht zugrunde gegangen.

                Sie warten nur darauf, dass der Nordwind wieder schwächer wird.
                """
            ).strip(),
            "seo_title": "",
            "seo_description": "",
            "is_published": True,
        },
        {
            "locale": "es",
            "title": "El Otoño Rojo",
            "slug": "el-otono-rojo",
            "excerpt": (
                "De la “Esfera de Shaftar”. Solo está permitido contar esta "
                "leyenda cuando el viento del norte aúlla con especial ferocidad. "
                "Si la cuentas fuera de tiempo, el viento puede arrebatarte la "
                "voz para siempre."
            ),
            "body": dedent(
                """
                En aquellos días, cuando el Señor del Mar apenas empezaba a enseñar a los hombres a temer su ira, y el patrono Shaftar ya gobernaba las montañas y minas del norte, llegó desde el mar una desgracia que ni siquiera los dioses esperaban.

                Aparecieron de noche.

                Cinco barcos negros con velas del color de la sangre fresca.

                A bordo iban guerreros cuyo cabello ardía rojizo como cobre fundido en la fragua del patrono. Su piel era más blanca que la nieve de las cumbres, y sus ojos eran negros, sin pupilas, como dos agujeros abiertos al abismo. No gritaban. No hacían sonar cuernos. Simplemente avanzaban hacia las rocas, como si supieran que las rocas no podrían detenerlos.

                La gente de la costa, donde entonces se alzaban las primeras aldeas pesqueras de Shaftar, los vio y comprendió: no eran invasores. Eran un castigo.

                Los pelirrojos no saqueaban. No tomaban esclavos. Reescribían todo lo vivo. Allí donde pisaban, la tierra se volvía roja, como empapada en sangre. Los árboles empezaban a derramar savia carmesí, y las personas a las que tocaban se convertían en cuestión de instantes en estatuas de madera: la piel se agrietaba, los huesos se volvían corteza, los ojos se endurecían en gotas de resina. Los vivos seguían gritando dentro de aquellas estatuas, pero ya no podían moverse.

                Se llamaban a sí mismos los Hijos del Invierno Carmesí. Decían que habían venido a reclamar la Isla para devolverla a la noche eterna y al frío eterno, donde no habría ni Señores ni Patronos.

                Su caudillo, un gigantesco coloso pelirrojo llamado Hjoelm, llevaba en el cinturón un collar de lenguas humanas y afirmaba que cada lengua le había suplicado piedad alguna vez... y aun así él la había tomado.

                Shaftar, patrono del viento del norte, montó en verdadera cólera.

                Desató sobre ellos toda la fuerza de su furia, un huracán tan terrible que las montañas de Shaftar aún llevan sus cicatrices. Los barcos quedaron hechos astillas. Los guerreros fueron arrojados contra los peñascos afilados como hojas secas. Durante muchos días el mar siguió rojo. Fue entonces cuando aquella costa recibió el nombre de la Costa de los Esqueletos de Madera, porque los cuerpos de los pelirrojos, destrozados contra las rocas, se petrificaron durante la noche y parecían árboles torcidos y retorcidos. Y los sacerdotes dieron al acontecimiento su nombre: el Otoño Rojo.

                Pero cinco sobrevivieron.

                No solo siguieron con vida. Lograron escapar.

                Cinco de los más terribles, aquellos que incluso en la agonía seguían enseñando sus bocas negras y desdentadas en una mueca. Se internaron en las grietas más profundas de las montañas septentrionales de Shaftar, allí donde ni siquiera las minas habían excavado. Allí fundaron un pequeño asentamiento llamado Valkha, un lugar donde, hasta el día de hoy, el viento del norte no canta la canción de Shaftar, sino su propia nana.

                Dicen que sus descendientes aún viven en Valkha.

                No envejecen como los hombres. Su cabello sigue siendo rojizo incluso en la tumba. Y si en noche de luna llena alguien se acerca demasiado al extremo septentrional de la tierra, oirá desde debajo del suelo un susurro suave, casi tierno:

                “Volveremos.
                No todos de una vez.
                Pero volveremos.”

                Por eso, en la provincia de Shaftar, sigue existiendo una ley: cualquier persona pelirroja debe o bien afeitarse la cabeza por completo, o bien marchar voluntariamente a las minas. Porque los sacerdotes recuerdan: los pelirrojos no perecieron.

                Solo están esperando a que el viento del norte vuelva a debilitarse.
                """
            ).strip(),
            "seo_title": "",
            "seo_description": "",
            "is_published": True,
        },
    ],
}


def _get_existing_parent(TranslationModel, parent_field_name, translations, db_alias):
    for translation in translations:
        existing = (
            TranslationModel.objects.using(db_alias)
            .select_related(parent_field_name)
            .filter(locale=translation["locale"], slug=translation["slug"])
            .first()
        )
        if existing is not None:
            return getattr(existing, parent_field_name)
    return None


def _upsert_catalog(CatalogModel, TranslationModel, parent_field_name, payload, db_alias):
    parent = _get_existing_parent(
        TranslationModel,
        parent_field_name,
        payload["translations"],
        db_alias,
    )
    if parent is None:
        parent = CatalogModel.objects.using(db_alias).create()

    for translation in payload["translations"]:
        TranslationModel.objects.using(db_alias).update_or_create(
            **{parent_field_name: parent, "locale": translation["locale"]},
            defaults={
                "name": translation["name"],
                "slug": translation["slug"],
                "description": translation["description"],
                "is_published": translation["is_published"],
            },
        )
    return parent


def _upsert_legend(LegendModel, LegendTranslationModel, payload, related_objects, db_alias):
    legend = _get_existing_parent(
        LegendTranslationModel,
        "legend",
        payload["translations"],
        db_alias,
    )
    if legend is None:
        legend = LegendModel.objects.using(db_alias).create()

    legend.status = payload["status"]
    legend.published_at = payload["published_at"]
    legend.hero_image = payload["hero_image"]
    legend.series = related_objects["series"]
    legend.province = related_objects["province"]
    legend.patron = related_objects["patron"]
    legend.save(using=db_alias)

    for translation in payload["translations"]:
        LegendTranslationModel.objects.using(db_alias).update_or_create(
            legend=legend,
            locale=translation["locale"],
            defaults={
                "title": translation["title"],
                "slug": translation["slug"],
                "excerpt": translation["excerpt"],
                "body": translation["body"],
                "seo_title": translation["seo_title"],
                "seo_description": translation["seo_description"],
                "is_published": translation["is_published"],
            },
        )

    legend.tags.set(related_objects["tags"])


def seed_minimal_content(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Series = apps.get_model("legends", "Series")
    Province = apps.get_model("legends", "Province")
    Patron = apps.get_model("legends", "Patron")
    Tag = apps.get_model("legends", "Tag")
    SeriesTranslation = apps.get_model("legends", "SeriesTranslation")
    ProvinceTranslation = apps.get_model("legends", "ProvinceTranslation")
    PatronTranslation = apps.get_model("legends", "PatronTranslation")
    TagTranslation = apps.get_model("legends", "TagTranslation")
    Legend = apps.get_model("legends", "Legend")
    LegendTranslation = apps.get_model("legends", "LegendTranslation")

    series = _upsert_catalog(
        Series,
        SeriesTranslation,
        "series",
        SERIES_SEED,
        db_alias,
    )
    province = _upsert_catalog(
        Province,
        ProvinceTranslation,
        "province",
        PROVINCE_SEED,
        db_alias,
    )
    patron = _upsert_catalog(
        Patron,
        PatronTranslation,
        "patron",
        PATRON_SEED,
        db_alias,
    )
    tags = [
        _upsert_catalog(Tag, TagTranslation, "tag", payload, db_alias)
        for payload in TAG_SEEDS
    ]

    _upsert_legend(
        Legend,
        LegendTranslation,
        LEGEND_SEED,
        {
            "series": series,
            "province": province,
            "patron": patron,
            "tags": tags,
        },
        db_alias,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("legends", "0003_publish_existing_taxonomy_translations"),
    ]

    operations = [
        migrations.RunPython(seed_minimal_content, migrations.RunPython.noop),
    ]
