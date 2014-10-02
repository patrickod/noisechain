import re

class EmailParser():
    def __init__(self, email):
        self.email = email

    def parse_lines(self):
        # Ignoring multipart messages for the moment
        if self.email.is_multipart():
            return []
        # Split out into newlines
        raw_lines = self.email.get_payload().split('\n')

        # Filter out empty lines
        lines = filter(None, raw_lines)

        # Join adjacent lines if line ends with =
        joined = []
        for l1, l2 in zip(lines, lines[1:]):
            if re.match('.*=$', l1):
                joined.append(self._join_paired_lines(l1, l2))
            else:
                joined += [l1, l2]

        return joined

    def lines_without_quotes(self):
        lines = self.parse_lines()
        lines = filter(lambda l: not re.search('^>.*', l), lines)
        return lines

    def _join_paired_lines(self, l1, l2):
        """
        Join lines broken by wrapping with =
        """
        return l1[1:-1] + l2

if __name__ == "__main__":
    import mailbox
    dec_07 = mailbox.mbox('archives/noisebridge-discuss/2007-December.txt')
    mail = dec_07[0]

    print EmailParser(mail).lines_without_quotes()
