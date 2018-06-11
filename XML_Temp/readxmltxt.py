def read_xml(annotname, width, height):
    xml = ''
    for line in open(annotname):
        xml += line
    xml = BeautifulSoup(xml, 'lxml')
    objects = xml.find_all("object")
    data_label = []
    for obj in objects:
        annotation = []
        if obj.find('type').text == 'polygon':
            name = obj.find('name').text
            #truncated = int(obj.find('truncated').text)
            deleted = int(obj.find('deleted').text)
            _id = int(obj.find('id').text)
            verified = 1 # int(obj.find('verified').text)
            difficult = obj.find('difficult').text
            if not deleted and verified:
                # TODO: change it to read especifically on x1 y1 ...
                for pt in obj.find_all('pt'):
                    x = float(pt.find('x').text)
                    y = float(pt.find('y').text)
                    annotation.extend([x,y])
                name, difficult, annotation = read_safe([name, difficult, annotation], labelname, line, width, height)
                data_label.append([name, difficult, annotation])
    df = pd.DataFrame(data=data_label, columns=['type', 'difficult', 'annotation'])
    if VERBOSE:
        print(df)
    if len(df) <= 0:
        warnings.warn("no objects in the label file", UserWarning)
        return
    print("xml was read")
    return df


def read_txt(labelname, width, height):

    # Get the filename where to load/save labels
    # Returns empty string if not possible
    # Set the createDirs to true, if you want to create needed directories
    file = open(labelname)
    data_label = []
    for line in file:
        if not (line[0] == 'g' or line[0] == 'i'):
            line = list(line.split(" "))
            if VERBOSE:
                print(line)
            name = line[8]
            # strange thing is dota txt, difficult parameter is together with '\n' and we have to use [9][0]
            difficult = int(line[9][0])
            annotation = line[0:8]
            name, difficult, annotation, passed = read_safe([name, difficult, annotation], labelname, line, width, height)
            if passed:
                data_label.append([name, difficult, annotation])
    dff = pd.DataFrame(data=data_label, columns=['type', 'difficult', 'annotation'])
    if VERBOSE:
        print(dff)
    if len(dff) <= 0:
        warnings.warn("no objects in the label file", UserWarning)
        return
    print("txt was read")
    return dff


def read_safe(tocheck, filename, readline, width, height):
    # tocheck[0]  is name
    # tocheck[1]  is difficulty
    # tocheck[2]  is annotation
    tocheck[2] = list(map(int, tocheck[2]))
    xs = tocheck[2][0:8:2]
    ys = tocheck[2][1:9:2]
    passed = True
    if sum(1 for number in tocheck[2] if number < 0):
        # no negative is tolerated
        print(filename)
        print(readline)
        print(tocheck)
        print(width)
        print(height)
        raise AssertionError("negative, ignored!")
        # warnings.warn("negative or violated size ", UserWarning)
    elif sum(1 for number in xs if number > width + 3) > 2: #TODO 3) > 2:
        # three pixel violation is tolerated
        print(filename)
        print(readline)
        print(tocheck)
        print(width)
        print(height)
        # TODO clamp three  pixel violation to width
        #if not 'P0173' in filename and xs[3] == 2103:  # P0173 has sample harbor with 2 pixel higher than width
        #raise AssertionError("violated width with more than two pixels")
        warnings.warn("violated size with {} pixel".format(xs), UserWarning)
        passed = False
    elif sum(1 for number in ys if number > height + 3) > 2: #TODO 3) > 2:
        # three pixel violation is tolerated
        print(filename)
        print(readline)
        print(tocheck)
        print(width)
        print(height)
        # TODO clamp three pixel violation to height
        # raise AssertionError("violated height with more than two pixels")
        warnings.warn("negative or violated size ", UserWarning)
        passed = False

        # indices = [line[i]='1' for i, line_ in enumerate(line[0:8]) if line_ in '0']
    if 0 in map(int, tocheck[2]):
        for i, line_ in enumerate(tocheck[2]):
            # if sum(1 for number in tocheck[2] if number == 0) > 1:
            if sum(1 for number in xs  if number == 0) > 2:
                raise AssertionError("WARNING: many x zeroes, ignored!")
            if sum(1 for number in xs  if number == 0) > 2:
                raise AssertionError("WARNING: many y zeroes, ignored!")
            if line_ == 0:
                tocheck[2][i] = 1
                if VERBOSE:
                    print(readline)
                    print(tocheck)
                    print(width)
                    print(height)
                    print(filename)
                # raise AssertionError("WARNING: one sample has parameter equal to zero, ignored!")
                # no warning for at most two zeros as there are quite some in dota dataset.
                # warnings.warn("One sample has parameter annotation equal to zero, ignored! ", UserWarning)
                # continue

    xmin, ymin, xmax, ymax = min(xs), min(ys), max(xs), max(ys)
    width_obj = xmax - xmin
    height_obj = ymax - ymin
    if not (2 < width_obj < width - 1 and 5 < height_obj < height - 1): #TODO or 10<=
        print(filename)
        print(readline)
        print(width_obj)
        print(height_obj)
        print(width)
        print(height)
        # raise AssertionError("double check width and height violated image size, ignored!")
        # TODO I noticed the minium width is 3 and also many of not passed ones were with width or height of 4 or 5.
        # maybe we could decrease the lower bound to 4.
        warnings.warn("WARNING: double check width and height violated image size, ignored!", UserWarning)
        passed = False
    return tocheck[0], tocheck[1], tocheck[2], passed

