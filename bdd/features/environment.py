def before_all(context):
    print('helllo')


def before_feature(context, feature):
    print(f'before feature {feature.name}')


def before_scenario(context, scenario):
    print('SCENARRRRIO')