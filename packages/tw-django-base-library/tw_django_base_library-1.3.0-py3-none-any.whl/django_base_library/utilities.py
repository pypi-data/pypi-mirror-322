class APIPaginatorParams:

    def checkEntries(self, params=None):

        if 'entries' in params:
            entries = params.get('entries')

            if not entries:
                entries = None

        else:
            entries = None

        return entries


    def checkPageNo(self, params=None):

        if 'page_no' in params:
            page_no = params.get('page_no')

            if not page_no:
                page_no = 1

        else:
            page_no = 1

        return page_no

