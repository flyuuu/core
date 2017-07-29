# ChEMBL blast api 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport requests123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport urllib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport http.cookiejar123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tempfile123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport json123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef chembl_blast(seq):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Get the blast result of the input sequence from ChEMBL server123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        seq ::str 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            AMINO ACID sequence123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            e.g. 'AINVLVCWAVWLNLQNNYFVVSLAAADIAVGVLAPFFFLKIWF'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        results :: list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            Blast result 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [ChEMBL_ID, Pref_Name, ProteinAccession_ID, Identity, Blast_Score, Evalue]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create connection123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cookie = http.cookiejar.CookieJar()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    handler = urllib.request.HTTPCookieProcessor(cookie)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    opener = urllib.request.build_opener(handler)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    opener.open('https://www.ebi.ac.uk/')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # encode data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    postdata = urllib.parse.urlencode({'seq':seq,'seg':'true'})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    binary_data = postdata.encode('utf-8')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # get the blast idx from server123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    opener.open('https://www.ebi.ac.uk/chembl/target/blast', binary_data)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    get_result = opener.open('https://www.ebi.ac.uk/chembl/index.php/target/results/blast')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cont = get_result.read().decode('utf-8')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    reg = r'/chembl//starlite/fetch_statistics/(\d+)'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    me = re.search(reg, cont)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # retrive blast result from server123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if me is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = me.groups()[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        blast_result = opener.open('https://www.ebi.ac.uk/chembl/target/data/blast?sEcho=1&iColumns=13&sColumns=&iDisplayStart=10&iDisplayLength=10&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&mDataProp_10=10&mDataProp_11=11&mDataProp_12=12&iSortCol_0=11&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&bSortable_7=true&bSortable_8=true&bSortable_9=true&bSortable_10=true&bSortable_11=true&bSortable_12=false&_=%s' % idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data = json.loads(blast_result.read())['aaData']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # result contain the following columns123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # query sequence | ChEMBL ID | TID | pref name | ProteinAccession ID | Target type | Organism | Comppuounds | Endpoints | Identity | Blast Score | Evalue | Tag123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        results = map(lambda datum:[datum[1], datum[3], datum[4], datum[9], datum[10], datum[11]],data)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        head = ['ChEMBL_ID', 'Pref_Name', 'ProteinAccession_ID', 'Identity', 'Blast_Score', 'Evalue']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return head, list(results)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception("Cannot retrive blast idx")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _, result = chembl_blast('AINVLVCWAVWLNLQNNYFVVSLAAADIAVGVLAPFFFLKIWF')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for entry in result:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print (entry)